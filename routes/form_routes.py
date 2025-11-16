"""
Form Routes - Medical Information Form
File: routes/form_routes.py
"""

from flask import Blueprint, render_template, request, jsonify
import json
import os

# Create Blueprint
form_bp = Blueprint('form', __name__)

# Data file path
DATA_FILE = 'form.json'

# ============================================
# FORM ROUTES
# ============================================

@form_bp.route('/form', methods=['GET'])
def form_page():
    """Show form page"""
    return render_template('form.html')

@form_bp.route('/form', methods=['POST'])
def form_submit():
    """Handle form submission"""
    user_data = {
        "name": request.form.get("name"),
        "age": request.form.get("age"),
        "weight": request.form.get("weight"),
        "gender": request.form.get("gender"),
        "medical_conditions": request.form.get("medical_conditions"),
        "medications": request.form.get("medications"),
        "height": request.form.get("height"),
        "smoker": request.form.get("smoker"),
        "alcohol": request.form.get("alcohol"),
        "allergies": request.form.get("allergies")
    }
    
    # Load existing data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    # Add new data
    data.append(user_data)
    
    # Save to file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Form data received: {user_data}")
    
    return jsonify({
        'success': True,
        'message': 'Form submitted successfully'
    })