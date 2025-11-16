"""
Authentication Routes - Login, Signup, Password Reset
File: routes/auth_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
import hashlib
from models.database import USERS_DATABASE
from utils.helpers import validate_reset_token, invalidate_reset_token, update_user_password

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# ============================================
# SIGNUP ROUTES
# ============================================

@auth_bp.route('/signup', methods=['GET'])
def signup_page():
    """Show signup page"""
    if 'user_id' in session:
        return redirect('/profile')
    
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def signup_submit():
    """Create new account"""
    fullname = request.form.get('fullname', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm-password', '')
    
    errors = []
    
    # Validation
    if not fullname:
        errors.append('Full name is required')
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')
    if not confirm_password:
        errors.append('Please confirm your password')
    
    if fullname and (len(fullname) < 2 or len(fullname) > 100):
        errors.append('Name must be between 2 and 100 characters')
    
    if email and '@' not in email:
        errors.append('Invalid email format')
    
    if email and email in USERS_DATABASE:
        errors.append('Email already registered')
    
    if password and len(password) < 8:
        errors.append('Password must be at least 8 characters')
    
    if password and confirm_password and password != confirm_password:
        errors.append('Passwords do not match')
    
    if errors:
        return render_template('signup.html', 
                             errors=errors,
                             fullname=fullname, 
                             email=email)
    
    # Create user
    user_id = len(USERS_DATABASE) + 1
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    USERS_DATABASE[email] = {
        'user_id': user_id,
        'fullname': fullname,
        'email': email,
        'password': hashed_password
    }
    
    print(f"New user created: {email}")
    
    session['signup_success'] = True
    return redirect('/login')

@auth_bp.route('/api/auth/check-email', methods=['GET', 'POST'])
def check_email():
    """Check if email exists"""
    if request.method == 'GET':
        email = request.args.get('email', '').strip().lower()
    else:
        email = request.form.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email required'}), 400
    
    if email in USERS_DATABASE:
        return jsonify({'available': False, 'message': 'Email already in use'})
    
    return jsonify({'available': True, 'message': 'Email is available'})

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
    """Login user"""
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
    
    if email not in USERS_DATABASE:
        errors.append('Invalid email or password')
        return render_template('login.html', errors=errors, email=email)
    
    user = USERS_DATABASE[email]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if user['password'] != hashed_password:
        errors.append('Invalid email or password')
        return render_template('login.html', errors=errors, email=email)
    
    # Login successful
    session['user_id'] = user['user_id']
    session['username'] = user['fullname']
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
    # Logic to send reset link would go here
    return jsonify({'success': True, 'message': 'Password reset link sent to your email'})

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