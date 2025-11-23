"""
Test MongoDB Connection and Saving
Run this to test if MongoDB is working
"""

from models.medicine_model import MedicineModel
import json


print("=" * 50)
print("🧪 TESTING MONGODB CONNECTION")
print("=" * 50)

# Initialize model
print("\n1️⃣ Creating MedicineModel...")
model = MedicineModel()
print("✅ Model created")

# Test data
test_medicine = {
    'name': 'Test Medicine',
    'description': 'This is a test medicine to verify MongoDB is working.',
    'advice': '• Take with water\n• Take after meals',
    'warning': '• Do not overdose\n• Consult doctor if symptoms persist',
    'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=test'
}

print("\n2️⃣ Test data:")
print(json.dumps(test_medicine, indent=2))

# Try to save
print("\n3️⃣ Attempting to save to MongoDB...")
try:
    medicine_id = model.create_medicine(test_medicine)
    print(f"✅ SUCCESS! Saved with ID: {medicine_id}")
except Exception as e:
    print(f"❌ FAILED to save: {e}")
    import traceback
    traceback.print_exc()

# Try to retrieve
print("\n4️⃣ Attempting to retrieve from MongoDB...")
try:
    result = model.get_medicine_by_name('Test Medicine')
    if result:
        print(f"✅ SUCCESS! Found medicine:")
        print(json.dumps(result, indent=2, default=str))
    else:
        print("❌ Medicine not found in database")
except Exception as e:
    print(f"❌ FAILED to retrieve: {e}")
    import traceback
    traceback.print_exc()

# Count all medicines
print("\n5️⃣ Counting all medicines in database...")
try:
    all_medicines = model.get_all_medicines()
    print(f"✅ Total medicines in database: {len(all_medicines)}")
    print("\nMedicines found:")
    for med in all_medicines:
        print(f"  - {med.get('name', 'Unknown')}")
except Exception as e:
    print(f"❌ FAILED to count: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🏁 TEST COMPLETE")
print("=" * 50)

# Close connection
model.close_connection()
