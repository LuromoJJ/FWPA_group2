"""
MongoDB Model for Medicine Storage
Replaces JSON file storage with MongoDB database
"""
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class MedicineModel:
    def __init__(self):
        # Get MongoDB connection from environment variables
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('DATABASE_NAME', 'medinfo_db')
        
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['Medicine']  # Your collection name
    
    def create_medicine(self, medicine_data):
        """
        Add a new medicine to the database
        
        Args:
            medicine_data (dict): Medicine information with keys:
                - name: Medicine name
                - description: Simple description
                - advice: Usage advice (list or string)
                - warning: Warnings (list or string)
                - pubmed_link: Link to research
                
        Returns:
            str: ID of inserted medicine
        """
        result = self.collection.insert_one(medicine_data)
        return str(result.inserted_id)
    
    def get_all_medicines(self):
        """
        Get all medicines from database
        
        Returns:
            list: All medicines with _id converted to string
        """
        medicines = list(self.collection.find({}))
        # Convert ObjectId to string for JSON
        for medicine in medicines:
            medicine['_id'] = str(medicine['_id'])
        return medicines
    
    def get_medicine_by_name(self, medicine_name):
        """
        Find medicine by name (case-insensitive)
        
        Args:
            medicine_name (str): Name to search for
            
        Returns:
            dict: Medicine data or None if not found
        """
        medicine = self.collection.find_one({
            'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}
        })
        if medicine:
            medicine['_id'] = str(medicine['_id'])
        return medicine
    
    def get_medicine_by_id(self, medicine_id):
        """
        Get a medicine by MongoDB ID
        
        Args:
            medicine_id (str): MongoDB ObjectId as string
            
        Returns:
            dict: Medicine data or None
        """
        try:
            medicine = self.collection.find_one({'_id': ObjectId(medicine_id)})
            if medicine:
                medicine['_id'] = str(medicine['_id'])
            return medicine
        except:
            return None
    
    def update_medicine(self, medicine_id, medicine_data):
        """
        Update existing medicine
        
        Args:
            medicine_id (str): MongoDB ID
            medicine_data (dict): Updated data
            
        Returns:
            bool: True if updated successfully
        """
        try:
            # Remove _id from update data
            medicine_data.pop('_id', None)
            result = self.collection.update_one(
                {'_id': ObjectId(medicine_id)},
                {'$set': medicine_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_medicine(self, medicine_id):
        """
        Delete a medicine from database
        
        Args:
            medicine_id (str): MongoDB ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            result = self.collection.delete_one({'_id': ObjectId(medicine_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def search_medicines(self, search_term):
        """
        Search medicines by name (partial match)
        
        Args:
            search_term (str): Text to search for
            
        Returns:
            list: Matching medicines
        """
        medicines = list(self.collection.find({
            'name': {'$regex': search_term, '$options': 'i'}
        }))
        for medicine in medicines:
            medicine['_id'] = str(medicine['_id'])
        return medicines
    
    def medicine_exists(self, medicine_name):
        """
        Check if medicine exists in database
        
        Args:
            medicine_name (str): Name to check
            
        Returns:
            bool: True if exists
        """
        count = self.collection.count_documents({
            'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}
        })
        return count > 0
    
    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()