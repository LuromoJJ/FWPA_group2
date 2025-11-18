"""
Medicine Routes - Updated to use MongoDB
File: routes/medicine_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
from models.medicine_model import MedicineModel  # ← Import MongoDB model
from utils.helpers import get_current_user
from utils.ai_service import generate_medicine_info
import threading

medicine_bp = Blueprint('medicine', __name__)

# Initialize MongoDB model
medicine_model = MedicineModel()

# Track which medicines are being generated
ai_status = {}

# ============================================
# HOMEPAGE
# ============================================

@medicine_bp.route('/')
@medicine_bp.route('/homepage')
def homepage():
    user_info = get_current_user()
    return render_template('homepage.html', user=user_info)

@medicine_bp.route('/search', methods=['POST'])
def search_medicine():
    medicine_name = request.form.get('medicine', '').strip()
    if not medicine_name:
        return jsonify({'error': 'Medicine name required'}), 400
    
    medicine_url = medicine_name.lower().replace(' ', '-')
    return redirect(f'/medicine/{medicine_url}')

# ============================================
# MEDICINE PAGE - Main Logic
# ============================================

@medicine_bp.route('/medicine/<name>')
def medicine_details(name):
    medicine_name = name.lower().replace('-', ' ')
    
    # Check if medicine exists in MongoDB
    medicine_data = medicine_model.get_medicine_by_name(medicine_name)
    
    if medicine_data:
        # Medicine found! Show it
        user_info = get_current_user()
        return render_template('medicine.html', medicine=medicine_data, user=user_info)
    
    # Medicine not found - need AI to generate it
    status = ai_status.get(medicine_name, 'new')
    
    if status == 'new':
        # First time - start AI generation
        ai_status[medicine_name] = 'working'
        thread = threading.Thread(target=generate_ai_info, args=(medicine_name,))
        thread.daemon = True
        thread.start()
    
    # Show loading message
    loading_data = {
        'name': name.replace('-', ' ').title(),
        'description': '🤖 AI is generating information... Please wait 1-3 minutes.',
        'advice': '⏳ Page will refresh automatically every 10 seconds.',
        'warning': '💡 Make sure LM Studio is running!',
        'pubmed_link': f'https://pubmed.ncbi.nlm.nih.gov/?term={name.replace("-", "+")}'
    }
    
    user_info = get_current_user()
    return render_template('medicine.html', medicine=loading_data, user=user_info)

# Background function to generate medicine info
def generate_ai_info(medicine_name):
    print(f"🤖 Starting AI for: {medicine_name}")
    
    # Call AI
    medicine_data = generate_medicine_info(medicine_name)
    
    if medicine_data:
        print(f"✅ AI done for: {medicine_name}")
        # Save to MongoDB instead of JSON
        medicine_model.create_medicine(medicine_data)
        ai_status[medicine_name] = 'done'
    else:
        print(f"❌ AI failed for: {medicine_name}")
        ai_status[medicine_name] = 'failed'

# ============================================
# ADD TO PROFILE
# ============================================

@medicine_bp.route('/api/profile/add-medicine', methods=['POST'])
def add_medicine_to_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please login first'}), 401
    
    medicine_name = request.form.get('medicine_name', '').strip().lower()
    
    # Check if medicine exists in MongoDB
    medicine_data = medicine_model.get_medicine_by_name(medicine_name)
    
    if not medicine_data:
        return jsonify({'success': False, 'error': 'Medicine not found'}), 404
    
    if 'saved_medicines' not in session:
        session['saved_medicines'] = []
    
    if medicine_name in session['saved_medicines']:
        return jsonify({'success': False, 'message': 'Already saved'}), 400
    
    session['saved_medicines'].append(medicine_name)
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'{medicine_data["name"]} added to profile'
    })

# ============================================
# REDIRECT OLD .html FILES
# ============================================

@medicine_bp.route('/<path:filename>.html')
def block_html_files(filename):
    if filename == 'homepage':
        return redirect('/')
    elif filename == 'login':
        return redirect('/login')
    elif filename == 'signup':
        return redirect('/signup')
    else:
        return redirect('/')

# ============================================
# CLOSE CONNECTION WHEN APP STOPS
# ============================================

@medicine_bp.teardown_app_request
def close_db_connection(exception=None):
    """Close MongoDB connection when request ends"""
    pass  # Connection pooling handles this automatically