"""
Form Routes - Medical Information Form
File: routes/form_routes.py
"""
from flask import Blueprint, render_template, request, session, redirect, jsonify
from models.user_model import DB

form_bp = Blueprint('form', __name__)

@form_bp.route('/form', methods=['GET'])
def form_page():
    if 'email' not in session:
        return redirect('/signup')

    db = DB()
    user_model = db.users
    user = user_model.get_user_by_email(session['email'])
    db.close()

    return render_template('form.html', user=user)

@form_bp.route('/form', methods=['POST'])
def form_submit():
    if 'email' not in session:
        return redirect('/signup')

    email = session['email']
    form_data = {
        "fullname": request.form.get("name"),
        "age": request.form.get("age"),
        "weight": request.form.get("weight"),
        "height": request.form.get("height"),
        "gender": request.form.get("gender"),
        "allergies": request.form.get("allergies"),
        "medications": request.form.get("medications"),
        "smoker": request.form.get("smoker"),
        "alcohol": request.form.get("alcohol"),
        "medical_conditions": request.form.get("medical_conditions")
    }

    db = DB()
    user_model = db.users
    user_model.update_user(email, form_data)

    medications = request.form.get("medications", "").strip()
    if medications:
        meds_list = [m.strip() for m in medications.split(",") if m.strip()]
        saved_meds_model = db.saved_meds
        for med in meds_list:
            saved_meds_model.save_medication(email, med)

    db.close()
    return redirect('/profile_page')