from flask import Blueprint, render_template, session, redirect, request
from models.user_model import DB
from datetime import datetime

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar', methods=['GET'])
def calendar_page():
    """Render the calendar page with the user's medicine schedule."""
    
    email = session.get('email')
    if not email:
        return redirect('/login')
    
    db = DB()
    scheduled_meds_model = db.scheduled_meds
    
    # Fetch schedule for this user by email
    raw_schedule = scheduled_meds_model.get_schedule_by_email(email)
    db.close()
    
    # Convert to plain dicts for JS
    schedule = []
    for med in raw_schedule:
        schedule.append({
            "medication": med.get("medication", ""),
            "schedule_time": med.get("schedule_time", "")
        })
    
    return render_template('calendar.html', schedule=schedule)

@calendar_bp.route('/schedule/add', methods=['GET', 'POST'])
def add_schedule():
    email = session.get('email')
    if not email:
        return redirect('/login')

    if request.method == 'POST':
        medication = request.form.get('medication')
        schedule_time = request.form.get('schedule_time')  # Expecting ISO string

        if not medication or not schedule_time:
            return "Medication name and time are required.", 400

        # Save to MongoDB
        db = DB()
        db.scheduled_meds.schedule_medication(email, medication, schedule_time)
        db.close()

        return redirect('/calendar')  # Redirect back to calendar page

    # GET request: show the form
    return render_template('add_schedule.html')