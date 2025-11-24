from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib
import os

load_dotenv()

class UserModel:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        if not self.mongo_uri:
            raise ValueError("MONGO_URI not set in environment")

        # Single MongoClient
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["MedInfo"]
        self.collection = self.db["User_prefs"] 

        print("DEBUG MONGO_URI:", self.mongo_uri)
        print("DEBUG DATABASES:", self.client.list_database_names())
        print("DEBUG DB:", self.db.name)
        print("DEBUG COLLECTION:", self.collection.name)

    def create_user(self, user):
        user['email'] = user['email'].strip().lower()
        # Hash password here only once
        user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()
        print("DEBUG INSERT USER:", user)
        result = self.collection.insert_one(user)
        print("DEBUG INSERTED ID:", result.inserted_id)
        return result.inserted_id

    def get_user_by_email(self, email):
        return self.collection.find_one({"email": email.strip().lower()})

    def authenticate(self, email, password):
        email = email.strip().lower()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        return self.collection.find_one({"email": email, "password": hashed_pw})

    def update_user(self, email, update_data):
        email = email.strip().lower()
        return self.collection.update_one(
            {"email": email},
            {"$set": update_data}
        )

    def close(self):
        self.client.close()