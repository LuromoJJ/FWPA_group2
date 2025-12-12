from models.user_model import DB

# User email
user_email = "random@name.com"  

# Medication to save
medication_name = "Aspirin"

# Connect to DB
db = DB()
saved_meds_model = db.saved_meds

# Save the medication and get the MongoDB ObjectId
inserted_id = saved_meds_model.save_medication(user_email, medication_name)

# Close the DB connection
db.close()

print(f"Medication '{medication_name}' saved for '{user_email}' with MongoDB ObjectId: {inserted_id}")