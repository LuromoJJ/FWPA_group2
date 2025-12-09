"""
Profile Routes - User Profile Page
File: routes/profile_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
from models.user_model import DB

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile_page', methods=['GET', 'POST'])
def profile_page():
    if 'email' not in session:
        return redirect('/login')

    email = session['email']
    db = DB()
    user_model = db.users
    saved_meds_model = db.saved_meds

    # Fetch user data
    user = user_model.get_user_by_email(email)

    if request.method == 'POST':
        # Collect updated form data
        profile_data = {
            "fullname": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "weight": request.form.get("weight", "").strip(),
            "height": request.form.get("height", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "allergies": request.form.get("allergies", "").strip(),
            "medications": request.form.get("medications", "").strip(),
            "smoker": request.form.get("smoker", "").strip(),
            "alcohol": request.form.get("alcohol", "").strip(),
            "medical_conditions": request.form.get("medical_conditions", "").strip()
        }
        user_model.update_user(email, profile_data)

        # Save each medication individually
        medications_input = request.form.get("medications", "").strip()
        if medications_input:
            meds_list = [m.strip() for m in medications_input.split(",") if m.strip()]
            for med in meds_list:
                saved_meds_model.save_medication(email, med)

        # Refresh user object
        user = user_model.get_user_by_email(email)
        db.close()
        return jsonify({"success": True, "message": "Profile updated", "user": user})

    # GET request → display profile
    # Fetch saved medicines for this user
    raw_meds = saved_meds_model.get_meds_by_email(email)
    saved_meds_list = [{"medication": med.get("medication", "")} for med in raw_meds]

    db.close()
    return render_template('profile_page.html', user=user, saved_medicines=saved_meds_list)