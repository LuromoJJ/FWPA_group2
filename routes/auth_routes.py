"""
Authentication Routes - Login, Signup, Password Reset
File: routes/auth_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
import hashlib
from models.user_model import UserModel
from utils.helpers import validate_reset_token, invalidate_reset_token, update_user_password

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# ============================================
# SIGNUP ROUTES
# ============================================

@auth_bp.route('/signup', methods=['GET'])
def signup_page():
    if 'user_id' in session:
        return redirect('/profile_page')
    return render_template('signup.html')


@auth_bp.route('/signup', methods=['POST'])
def signup_submit():
    fullname = request.form.get('fullname', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm-password', '')

    errors = []

    if not fullname: errors.append('Full name is required')
    if not email: errors.append('Email is required')
    if not password: errors.append('Password is required')
    if not confirm_password: errors.append('Please confirm your password')
    if password != confirm_password: errors.append('Passwords do not match')
    if '@' not in email: errors.append('Invalid email')
    if len(password) < 8: errors.append('Password must be at least 8 characters')

    user_model = UserModel()
    if user_model.get_user_by_email(email):
        errors.append('Email already registered')

    if errors:
        user_model.close()
        return render_template('signup.html', errors=errors, fullname=fullname, email=email)

    # Hash password and create user
    user_doc = {
        'fullname': fullname,
        'email': email,
        'password': password  # Hash inside UserModel
    }
    new_user_id = user_model.create_user(user_doc)
    user_model.close()

    # Store session info
    session['user_id'] = str(new_user_id)
    session['email'] = email
    session['fullname'] = fullname

    # Redirect to extra info form
    return redirect('/form')
# ============================================
# LOGIN ROUTES
# ============================================
@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Show login page"""
    if 'user_id' in session:
        return redirect('/')
    
    signup_success = session.pop('signup_success', False)
    return render_template('login.html', signup_success=signup_success)

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    """Login user using MongoDB"""
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    remember = request.form.get('remember')

    errors = []

    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')

    if errors:
        return render_template('login.html', errors=errors, email=email)

    # Use MongoDB
    user_model = UserModel()
    user = user_model.authenticate(email, password)

    if not user:
        errors.append("Invalid email or password")
        return render_template('login.html', errors=errors, email=email)

    # Login successful → store in session
    session['user_id'] = str(user["_id"])
    session['username'] = user.get('fullname', '')
    session['email'] = user['email']

    if remember:
        session.permanent = True
    print(f"User logged in: {email}")

    return redirect('/')
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    session.clear()
    print("User logged out")
    return redirect('/')

@auth_bp.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check if user is logged in"""
    from utils.helpers import get_current_user
    user_info = get_current_user()
    return jsonify(user_info)

# ============================================
# PASSWORD RESET ROUTES
# ============================================

@auth_bp.route('/forgot_password', methods=['GET'])
def forgot_password_page():
    """Show forgot password page"""
    return render_template('forgot_password.html')

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password_submit():
    """Handle forgot password submission"""
    email = request.form.get('email', '').strip().lower()

    user_model = UserModel()
    user = user_model.get_user_by_email(email)
    user_model.close()

    if not user:
        return jsonify({'success': False, 'message': 'Email not found'}), 400

    # Generate token
    from utils.helpers import generate_reset_token, send_reset_email
    token = generate_reset_token(email)

    # Send email
    send_reset_email(email, token)

    return jsonify({'success': True, 'message': 'Password reset email sent'})

@auth_bp.route('/set_new_password/<token>', methods=['GET'])
def reset_password_page(token):
    """Show password reset page"""
    user_email = validate_reset_token(token)
    if not user_email:
        return "Invalid or expired token", 400
    
    return render_template('set_new_password.html', token=token)
    

@auth_bp.route('/set_new_password/<token>', methods=['POST'])
def reset_password_submit(token):
    """Handle password reset"""
    email = request.form.get('email', '').strip()
    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    
    errors = []
    
    user_email = validate_reset_token(token)
    if not user_email or user_email != email:
        errors.append("Invalid or expired token")
    
    if not new_password or len(new_password) < 8:
        errors.append("Password must be at least 8 characters long")
    if new_password != confirm_password:
        errors.append("Passwords do not match")
    
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    update_user_password(email, new_password)
    invalidate_reset_token(token)
    
    return jsonify({'success': True, 'message': 'Password updated successfully'})