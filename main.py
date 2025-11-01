"""
Flask Backend - Simple Version for Students
File: main.py
"""

from flask import Flask, render_template, request, jsonify, redirect, session
import os
import hashlib
import re

# ============================================
# FLASK APP SETUP
# ============================================

# Get absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'src')
STATIC_DIR = os.path.join(BASE_DIR, 'src')

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR,
            static_url_path='')
app.secret_key = 'key123'

# Debug: Print paths
print(f"Template folder: {TEMPLATE_DIR}")
print(f"Static folder: {STATIC_DIR}")

# ============================================
# SIMPLE DATABASES (in-memory - data lost on restart)
# ============================================

# Users database
USERS_DATABASE = {}

# Medicine database
MEDICINE_DATABASE = {
    'aspirin': {
        'name': 'Aspirin',
        'description': 'Aspirin (acetylsalicylic acid) is commonly used to reduce pain, fever, or inflammation. It can also help prevent heart attacks and strokes by reducing blood clotting. It should be taken with food or water and never on an empty stomach.',
        'advice': 'Take with food or milk to reduce stomach irritation. Avoid alcohol while using this medicine.',
        'warning': 'Do not mix with other blood-thinning medications. Avoid use if you have ulcers or bleeding disorders.',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=aspirin'
    },
    'ibuprofen': {
        'name': 'Ibuprofen',
        'description': 'Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to reduce fever and treat pain or inflammation.',
        'advice': 'Take with food or milk. Drink plenty of water.',
        'warning': 'May increase risk of heart attack or stroke. Avoid if you have stomach ulcers.',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=ibuprofen'
    },
    'paracetamol': {
        'name': 'Paracetamol',
        'description': 'Paracetamol (acetaminophen) is used to treat mild to moderate pain and to reduce fever.',
        'advice': 'Can be taken with or without food. Do not exceed recommended dose.',
        'warning': 'Overdose can cause severe liver damage. Avoid alcohol.',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=paracetamol'
    }
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_current_user():
    """Check if user is logged in"""
    if 'user_id' in session:
        return {
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'email': session.get('email')
        }
    return {'logged_in': False}

# ============================================
# HOMEPAGE ENDPOINTS
# ============================================

@app.route('/')
@app.route('/homepage')
def homepage():
    """Show homepage"""
    user_info = get_current_user()
    return render_template('homepage.html', user=user_info)

@app.route('/search', methods=['POST'])
def search_medicine():
    """Search for medicine"""
    medicine_name = request.form.get('medicine', '').strip()
    
    if not medicine_name:
        return jsonify({'error': 'Medicine name is required'}), 400
    
    # Clean name for URL
    medicine_url = medicine_name.lower().replace(' ', '-')
    return redirect(f'/medicine/{medicine_url}')

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check if user is logged in"""
    user_info = get_current_user()
    return jsonify(user_info)

# ============================================
# SIGNUP ENDPOINTS
# ============================================

@app.route('/signup', methods=['GET'])
def signup_page():
    """Show signup page"""
    # If already logged in, go to profile
    if 'user_id' in session:
        return redirect('/profile')
    
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_submit():
    """Create new account"""
    # Get form data
    fullname = request.form.get('fullname', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm-password', '')
    
    # List to collect errors
    errors = []
    
    # Check if fields are filled
    if not fullname:
        errors.append('Full name is required')
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')
    if not confirm_password:
        errors.append('Please confirm your password')
    
    # Check name length
    if fullname and (len(fullname) < 2 or len(fullname) > 100):
        errors.append('Name must be between 2 and 100 characters')
    
    # Check email format (simple check)
    if email and '@' not in email:
        errors.append('Invalid email format')
    
    # Check if email already exists
    if email and email in USERS_DATABASE:
        errors.append('Email already registered')
    
    # Check password length
    if password and len(password) < 8:
        errors.append('Password must be at least 8 characters')
    
    # Check if passwords match
    if password and confirm_password and password != confirm_password:
        errors.append('Passwords do not match')
    
    # If there are errors, show the form again with errors
    if errors:
        return render_template('signup.html', 
                             errors=errors,
                             fullname=fullname, 
                             email=email)
    
    # Create user ID
    user_id = len(USERS_DATABASE) + 1
    
    # Hash password (simple - use bcrypt in real projects!)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Save user
    USERS_DATABASE[email] = {
        'user_id': user_id,
        'fullname': fullname,
        'email': email,
        'password': hashed_password
    }
    
    print(f"New user created: {email}")  # Debug
    
    # Redirect to login
    session['signup_success'] = True
    return redirect('/login')

@app.route('/api/auth/check-email', methods=['GET', 'POST'])
def check_email():
    """Check if email exists"""
    # Get email
    if request.method == 'GET':
        email = request.args.get('email', '').strip().lower()
    else:
        email = request.form.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email required'}), 400
    
    # Check if exists
    if email in USERS_DATABASE:
        return jsonify({'available': False, 'message': 'Email already in use'})
    
    return jsonify({'available': True, 'message': 'Email is available'})

# ============================================
# LOGIN PAGE ENDPOINTS
# ============================================

@app.route('/login', methods=['GET'])
def login_page():
    """Show login page"""
    # If already logged in, go to homepage
    if 'user_id' in session:
        return redirect('/')
    
    # Check if user just signed up
    signup_success = session.pop('signup_success', False)
    
    return render_template('login.html', signup_success=signup_success)

@app.route('/login', methods=['POST'])
def login_submit():
    """Login user"""
    # Get form data
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    remember = request.form.get('remember')
    
    # List to collect errors
    errors = []
    
    # Check if fields are filled
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')
    
    # If there are errors, show the form again
    if errors:
        return render_template('login.html', errors=errors, email=email)
    
    # Check if user exists
    if email not in USERS_DATABASE:
        errors.append('Invalid email or password')
        return render_template('login.html', errors=errors, email=email)
    
    # Get user from database
    user = USERS_DATABASE[email]
    
    # Hash the entered password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Check if password matches
    if user['password'] != hashed_password:
        errors.append('Invalid email or password')
        return render_template('login.html', errors=errors, email=email)
    
    # Login successful! Create session
    session['user_id'] = user['user_id']
    session['username'] = user['fullname']
    session['email'] = user['email']
    
    # Set session to last longer if "remember me" is checked
    if remember:
        session.permanent = True
    
    print(f"User logged in: {email}")
    
    # Redirect to homepage
    return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    session.clear()
    print("User logged out")
    
    return redirect('/')

# ============================================
# MEDICINE PAGE ENDPOINTS
# ============================================

@app.route('/medicine/<name>')
def medicine_details(name):
    """Show medicine details"""
    # Clean medicine name
    medicine_name = name.lower().replace('-', ' ')
    
    # Find medicine
    medicine_data = MEDICINE_DATABASE.get(medicine_name)
    
    if not medicine_data:
        return jsonify({'error': f'Medicine "{name}" not found'}), 404
    
    # Get user info
    user_info = get_current_user()
    
    # Show medicine page
    return render_template('medicine.html', 
                         medicine=medicine_data,
                         user=user_info)

@app.route('/api/medicine/<name>', methods=['GET'])
def get_medicine_api(name):
    """Get medicine as JSON"""
    medicine_name = name.lower().replace('-', ' ')
    medicine_data = MEDICINE_DATABASE.get(medicine_name)
    
    if not medicine_data:
        return jsonify({'error': f'Medicine "{name}" not found'}), 404
    
    return jsonify(medicine_data)

@app.route('/api/profile/add-medicine', methods=['POST'])
def add_medicine_to_profile():
    """Save medicine to profile (requires login)"""
    # Check if logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please login first'}), 401
    
    # Get medicine name
    medicine_name = request.form.get('medicine_name', '').strip().lower()
    
    if not medicine_name:
        return jsonify({'success': False, 'error': 'Medicine name required'}), 400
    
    # Check if medicine exists
    if medicine_name not in MEDICINE_DATABASE:
        return jsonify({'success': False, 'error': 'Medicine not found'}), 404
    
    # Save to session (temporary)
    if 'saved_medicines' not in session:
        session['saved_medicines'] = []
    
    # Check if already saved
    if medicine_name in session['saved_medicines']:
        return jsonify({'success': False, 'message': 'Already saved'}), 400
    
    # Add to saved
    session['saved_medicines'].append(medicine_name)
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'{MEDICINE_DATABASE[medicine_name]["name"]} added to profile'
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Server error'}), 500

# ============================================
# REDIRECT .html FILES TO PROPER ROUTES
# ============================================

@app.route('/<path:filename>.html')
def block_html_files(filename):
    """Redirect .html files to proper routes"""
    if filename == 'homepage':
        return redirect('/')
    elif filename == 'login':
        return redirect('/login')
    elif filename == 'signup':
        return redirect('/signup')
    elif filename == 'medicine':
        return redirect('/')
    else:
        return redirect('/')

# ============================================
# STATIC FILE SERVING (Must be at the END!)
# ============================================

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    from flask import send_from_directory
    return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve images and other assets"""
    from flask import send_from_directory
    return send_from_directory(os.path.join(STATIC_DIR, 'assets'), filename)

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    print("\n=== Starting Flask Server ===")
    print("Homepage: http://localhost:5000/")
    print("Signup: http://localhost:5000/signup")
    print("Login: http://localhost:5000/login")
    print("Medicine: http://localhost:5000/medicine/aspirin")
    print("\nPress CTRL+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)


    #Forgot Password Endpoints (Not Implemented)

    @app.route('/forgot_password', methods=['GET'])
    def forgot_password_page():
        #Show forgot password page
        return render_template('forgot_password.html')
    
    @app.route('/forgot_password', methods=['POST'])
    def forgot_password_submit():
        # Handle forgot password submission
         email = request.form.get('email', '').strip().lower()
        # Logic to send reset link would go here
         return jsonify({'success': True, 'message': 'Password reset link sent to your email'})    
  
  
    #  Password Reset Endpoints

    @app.route('/set_new_password/<token>', methods=['GET'])
    def reset_password_page(token):
        #Show reset password page
         return render_template('set_new_password.html', token=token)
    
    @app.route('/set_newpassword/<token>', methods=['POST'])
    def reset_password_submit(token):
        #Handle reset password submission
         new_password = request.form.get('new_password', '')
         confirm_password = request.form.get('confirm_password', '')
        # Logic to reset password would go here
         if new_password != confirm_password:
             return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
         return jsonify({'success': True, 'message': 'Password has been reset successfully'})
    


    # Profile Page Endpoints 

    @app.route('/profile', methods=['GET'])
    def profile_page():
        #Show user profile page
        if 'user_id' not in session:
            return redirect('/login')
        user_info = get_current_user()
        saved_medicines = session.get('saved_medicines', [])
        medicines_data = [MEDICINE_DATABASE[name] for name in saved_medicines if name in MEDICINE_DATABASE]
        return render_template('profile.html', user=user_info, medicines=medicines_data)  
    @app.route('/profile', methods=['POST'])
    def profile_update():
        #Update user profile information
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Please login first'}), 401
        #Logic to update profile would go here
        return jsonify({'success': True, 'message': 'Profile updated successfully'})      
  
  