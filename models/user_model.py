
from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib
import os

load_dotenv()

class UserModel:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["MedInfo"]
        # Use user_prefs collection
        self.collection = self.db["user_prefs"]

    def create_user(self, user):
        """Insert a new user document"""
        return self.collection.insert_one(user).inserted_id

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.collection.find_one({"email": email})

    def authenticate(self, email, password):
        """Check if email + password match"""
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        return self.collection.find_one({"email": email, "password": hashed_pw})

    def update_user(self, email, update_data):
        """Update user preferences/data"""
        return self.collection.update_one(
            {"email": email},
            {"$set": update_data}
        )

    def close(self):
        """Close MongoDB connection"""
        self.client.close()