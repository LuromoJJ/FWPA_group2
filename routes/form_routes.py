"""
Form Routes - Medical Information Form
File: routes/form_routes.py
"""
from flask import Blueprint, render_template, request, session, redirect, jsonify
from models.user_model import UserModel

form_bp = Blueprint('form', __name__)

@form_bp.route('/form', methods=['GET'])
def form_page():
    if 'email' not in session:
        return redirect('/signup')

    user_model = UserModel()
    user = user_model.get_user_by_email(session['email'])
    user_model.close()

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

    user_model = UserModel()
    user_model.update_user(email, form_data)
    user_model.close()

    return redirect('/profile_page')