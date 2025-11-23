"""
Database Models - MongoDB Version
File: models/database.py
"""

from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import json

load_dotenv()

# ============================================
# MONGODB CONNECTION
# ============================================

mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
database_name = os.getenv('DATABASE_NAME', 'MedInfo')

client = MongoClient(mongodb_uri)
db = client[database_name]

# Collections
users_collection = db['users']
medicines_collection = db['Medicine'] 
reset_tokens_collection = db['reset_tokens']

print(f"✓ Connected to MongoDB at {mongodb_uri}, DB: {database_name}")

# ============================================
# USERS DATABASE (For backwards compatibility)
# ============================================

class UsersDatabase:
    """Wrapper to make MongoDB work like old USERS_DATABASE dict"""
    
    def get(self, email, default=None):
        """Get user by email"""
        user = users_collection.find_one({'email': email})
        return user if user else default
    
    def __setitem__(self, email, user_data):
        """Add or update user"""
        users_collection.update_one(
            {'email': email},
            {'$set': user_data},
            upsert=True
        )
    
    def __getitem__(self, email):
        """Get user by email (raises KeyError if not found)"""
        user = users_collection.find_one({'email': email})
        if user is None:
            raise KeyError(f"User {email} not found")
        return user
    
    def __contains__(self, email):
        """Check if user exists"""
        return users_collection.count_documents({'email': email}) > 0

USERS_DATABASE = UsersDatabase()

# ============================================
# MEDICINE DATABASE (For backwards compatibility)
# ============================================

class MedicineDatabase:
    """Wrapper to make MongoDB work like old MEDICINE_DATABASE dict"""
    
    def get(self, medicine_name, default=None):
        """Get medicine by name (case-insensitive)"""
        medicine = medicines_collection.find_one({
            'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}
        })
        return medicine if medicine else default
    
    def __setitem__(self, medicine_name, medicine_data):
        """Add or update medicine"""
        medicines_collection.update_one(
            {'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}},
            {'$set': medicine_data},
            upsert=True
        )
    
    def __getitem__(self, medicine_name):
        """Get medicine by name (raises KeyError if not found)"""
        medicine = medicines_collection.find_one({
            'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}
        })
        if medicine is None:
            raise KeyError(f"Medicine {medicine_name} not found")
        return medicine
    
    def __contains__(self, medicine_name):
        """Check if medicine exists"""
        return medicines_collection.count_documents({
            'name': {'$regex': f'^{medicine_name}$', '$options': 'i'}
        }) > 0

MEDICINE_DATABASE = MedicineDatabase()

# ============================================
# PASSWORD RESET TOKENS (For backwards compatibility)
# ============================================

class ResetTokensDatabase:
    """Wrapper for reset tokens"""
    
    def get(self, token, default=None):
        """Get token data"""
        token_data = reset_tokens_collection.find_one({'token': token})
        return token_data if token_data else default
    
    def __setitem__(self, token, token_data):
        """Add or update token"""
        token_data['token'] = token  # Add token to data
        reset_tokens_collection.update_one(
            {'token': token},
            {'$set': token_data},
            upsert=True
        )
    
    def __delitem__(self, token):
        """Delete token"""
        reset_tokens_collection.delete_one({'token': token})
    
    def __contains__(self, token):
        """Check if token exists"""
        return reset_tokens_collection.count_documents({'token': token}) > 0

RESET_TOKENS = ResetTokensDatabase()

# ============================================
# HELPER FUNCTION (Keeps old functionality)
# ============================================

def save_medicine_to_file(medicine_name, medicine_data):
    """
    Save medicine to MongoDB (replaces JSON file saving)
    Kept for backwards compatibility with old code
    """
    try:
        MEDICINE_DATABASE[medicine_name] = medicine_data
        print(f"✓ Saved '{medicine_name}' to MongoDB")
        return True
    except Exception as e:
        print(f"Error saving medicine: {e}")
        return False

# ============================================
# SEED DEFAULT MEDICINES (Run once)
# ============================================

def seed_default_medicines():
    """Add default medicines if database is empty"""
    
    # Check if medicines already exist
    if medicines_collection.count_documents({}) > 0:
        print(f"✓ Database already has {medicines_collection.count_documents({})} medicines")
        return
    
    print("📦 Seeding default medicines...")
    
    default_medicines = [
        {
            'name': 'Aspirin',
            'description': 'Aspirin is a common painkiller that helps reduce pain, fever, and inflammation in your body. It works by blocking chemicals that cause pain and swelling. Doctors also prescribe it to prevent heart attacks and strokes because it stops blood from clotting too much. You can buy it at any pharmacy without a prescription.',
            'advice': '• Take with food or a full glass of water\n• Don\'t take on an empty stomach\n• Take one tablet every 4-6 hours as needed\n• Don\'t take more than 8 tablets in 24 hours',
            'warning': '• Don\'t mix with other painkillers without asking a doctor\n• Avoid if you have stomach ulcers or bleeding problems\n• Don\'t drink alcohol while taking it\n• May cause stomach upset or bleeding in some people',
            'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=aspirin'
        },
        {
            'name': 'Ibuprofen',
            'description': 'Ibuprofen is a painkiller that helps with headaches, muscle aches, period pain, and fever. It belongs to a group of medicines called NSAIDs which reduce inflammation and pain in your body. It works by blocking chemicals that cause swelling and pain. You can buy it at pharmacies without a prescription for short-term use.',
            'advice': '• Take with food or milk to protect your stomach\n• Drink plenty of water with each dose\n• Take the lowest dose that works for you\n• Don\'t use for more than 10 days without seeing a doctor',
            'warning': '• Don\'t take if you have stomach problems or asthma\n• May increase risk of heart problems if used long-term\n• Avoid alcohol while taking this medicine\n• Can interact badly with blood pressure medicines',
            'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=ibuprofen'
        },
        {
            'name': 'Paracetamol',
            'description': 'Paracetamol (also called acetaminophen) is a very common medicine for pain and fever. It helps with headaches, toothaches, period pain, cold symptoms, and reducing high temperature. It\'s gentler on your stomach than other painkillers and is safe for most people when used correctly. You can buy it without a prescription.',
            'advice': '• Can take with or without food\n• Take one or two tablets every 4-6 hours as needed\n• Wait at least 4 hours between doses\n• Read the label carefully - many cold medicines also contain paracetamol',
            'warning': '• Never take more than 8 tablets (4000mg) in 24 hours\n• Taking too much can cause serious liver damage\n• Don\'t drink alcohol while taking this\n• Check other medicines don\'t also contain paracetamol',
            'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=paracetamol'
        }
    ]
    
    medicines_collection.insert_many(default_medicines)
    print(f"✅ Added {len(default_medicines)} default medicines")

# ============================================
# MIGRATE OLD JSON DATA (Run once)
# ============================================

def migrate_from_json_if_needed():
    """Migrate medicines from old JSON file to MongoDB"""
    
    json_file = os.path.join(os.path.dirname(__file__), '..', 'medicine_database.json')
    
    if not os.path.exists(json_file):
        return  # No old data to migrate
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            old_medicines = json.load(f)
        
        migrated = 0
        for medicine_name, medicine_data in old_medicines.items():
            # Check if already exists
            if medicine_name.lower() not in MEDICINE_DATABASE:
                medicines_collection.insert_one(medicine_data)
                migrated += 1
        
        if migrated > 0:
            print(f"✓ Migrated {migrated} medicines from {json_file} into MongoDB")
    
    except Exception as e:
        print(f"Error migrating JSON data: {e}")

# ============================================
# RUN ON STARTUP
# ============================================

# Seed default medicines if needed
seed_default_medicines()

# Migrate old JSON data if exists
migrate_from_json_if_needed()