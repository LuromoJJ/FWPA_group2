from models.user_model import DB
from datetime import datetime, timedelta

# Connect to DB
db = DB()
scheduled_meds = db.scheduled_meds

# Example test user
email = "testuser@example.com"

# Example medicine entry
medication = "Paracetamol"
# Schedule for today at 10:00 AM
schedule_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

# Insert entry
entry_id = scheduled_meds.schedule_medication(email, medication, schedule_time.isoformat())
print(f"Test schedule inserted with ID: {entry_id}")

# Close DB
db.close()