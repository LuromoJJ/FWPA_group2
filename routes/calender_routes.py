from flask import Blueprint, render_template, request, session, redirect, jsonify
from models.user_model import ScheduledMedsModel

calender_bp = Blueprint('calendar', __name__)


@calender_bp.route('/calendar', methods=['GET'])
def calendar_page():
    """Render the calendar page with the user's medicine schedule."""
    user_id = session.get('user_id')  # Ensure the user is logged in
    if not user_id:
        return redirect('/login')  # Redirect to login if not authenticated

    # Fetch the user's medicine schedule
    meds_model = ScheduledMedsModel()
    schedule = meds_model.get_schedule_by_user_id(user_id)
    meds_model.close()

    # Pass the schedule to the template
    return render_template('calender.html', schedule=schedule)