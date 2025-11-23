"""
Profile Routes - User Profile Page
File: routes/profile_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile_page', methods=['GET', 'POST'])
def profile_page():
    """Show and update user profile"""
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'GET':
        user_data = session.get('user_data', {
            "name": "",
            "age": "",
            "email": "",
            "weight": "",
            "height": "",
            "gender": "",
            "allergies": "",
            "medications": "",
            "smoker": "",
            "alcohol": ""
        })
        saved_medicines = session.get('saved_medicines', [])

        # Use the correct template name
        return render_template(
            'profile_page.html',
            user=user_data,
            saved_medicines=saved_medicines
        )

    elif request.method == 'POST':
        updated_data = {
            "name": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "email": request.form.get("email", "").strip(),
            "weight": request.form.get("weight", "").strip(),
            "height": request.form.get("height", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "allergies": request.form.get("allergies", "").strip(),
            "medications": request.form.get("medications", "").strip(),
            "smoker": request.form.get("smoker", "").strip(),
            "alcohol": request.form.get("alcohol", "").strip()
        }

        if not updated_data["email"] or "@" not in updated_data["email"]:
            return jsonify({'success': False, 'message': 'Invalid email'}), 400

        session['user_data'] = updated_data

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': updated_data
        })