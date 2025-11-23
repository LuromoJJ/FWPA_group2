from models.user_model import UserModel
from dotenv import load_dotenv
import hashlib
import json

load_dotenv()

print("=" * 50)
print("🧪 TESTING USER MONGODB CONNECTION")
print("=" * 50)

model = UserModel()

test_user = {
    "user_id": 1,
    "fullname": "Test User",
    "email": "test@example.com",
    "password": "1234",         
    "allergies": "Pollen",
    "gender": "Male",
    "prescriptions": "Metformin",
    "weight": "66"
}

# INSERT TEST USER
print("\n1️⃣ Inserting test user...")
try:
    result = model.create_user(test_user)
    print(f"✅ User inserted with ID: {result}")
except Exception as e:
    print("❌ Insert failed:", e)

# RETRIEVE BY EMAIL
print("\n2️⃣ Retrieving test user...")
try:
    found = model.get_user_by_email("test@example.com")
    print("✅ Retrieved user:")
    print(json.dumps(found, indent=2, default=str))
except Exception as e:
    print("❌ Retrieval failed:", e)

# AUTHENTICATE
print("\n3️⃣ Authenticating...")
try:
    auth = model.authenticate("test@example.com", "password123")
    if auth:
        print("✅ Authentication successful")
    else:
        print("❌ Authentication failed (wrong logic or not found)")
except Exception as e:
    print("❌ Auth failed:", e)

model.close()
print("\n🏁 USER TEST COMPLETE")