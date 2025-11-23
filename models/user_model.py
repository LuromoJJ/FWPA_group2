
from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib
import os

load_dotenv()

class UserModel:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["MedInfo"]
        self.collection = self.db["users"]

    def create_user(self, user):
        return self.collection.insert_one(user).inserted_id

    def get_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def authenticate(self, email, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        return self.collection.find_one({"email": email, "password": hashed_pw})

    def close(self):
        self.client.close()