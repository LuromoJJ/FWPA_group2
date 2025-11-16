"""
Medicine Routes - Homepage, Search, Medicine Details
File: routes/medicine_routes.py
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
from models.database import MEDICINE_DATABASE
from utils.helpers import get_current_user

# Create Blueprint
medicine_bp = Blueprint('medicine', __name__)

# ============================================
# HOMEPAGE ROUTES
# ============================================

@medicine_bp.route('/')
@medicine_bp.route('/homepage')
def homepage():
    """Show homepage"""
    user_info = get_current_user()
    return render_template('homepage.html', user=user_info)

@medicine_bp.route('/search', methods=['POST'])
def search_medicine():
    """Search for medicine"""
    medicine_name = request.form.get('medicine', '').strip()
    
    if not medicine_name:
        return jsonify({'error': 'Medicine name is required'}), 400
    
    medicine_url = medicine_name.lower().replace(' ', '-')
    return redirect(f'/medicine/{medicine_url}')

# ============================================
# MEDICINE DETAIL ROUTES
# ============================================

@medicine_bp.route('/medicine/<name>')
def medicine_details(name):
    """Show medicine details"""
    medicine_name = name.lower().replace('-', ' ')
    medicine_data = MEDICINE_DATABASE.get(medicine_name)
    
    if not medicine_data:
        return jsonify({'error': f'Medicine "{name}" not found'}), 404
    
    user_info = get_current_user()
    return render_template('medicine.html', 
                         medicine=medicine_data,
                         user=user_info)

@medicine_bp.route('/api/medicine/<name>', methods=['GET'])
def get_medicine_api(name):
    """Get medicine as JSON"""
    medicine_name = name.lower().replace('-', ' ')
    medicine_data = MEDICINE_DATABASE.get(medicine_name)
    
    if not medicine_data:
        return jsonify({'error': f'Medicine "{name}" not found'}), 404
    
    return jsonify(medicine_data)

# ============================================
# SAVE MEDICINE ROUTES
# ============================================

@medicine_bp.route('/api/profile/add-medicine', methods=['POST'])
def add_medicine_to_profile():
    """Save medicine to profile (requires login)"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please login first'}), 401
    
    medicine_name = request.form.get('medicine_name', '').strip().lower()
    
    if not medicine_name:
        return jsonify({'success': False, 'error': 'Medicine name required'}), 400
    
    if medicine_name not in MEDICINE_DATABASE:
        return jsonify({'success': False, 'error': 'Medicine not found'}), 404
    
    if 'saved_medicines' not in session:
        session['saved_medicines'] = []
    
    if medicine_name in session['saved_medicines']:
        return jsonify({'success': False, 'message': 'Already saved'}), 400
    
    session['saved_medicines'].append(medicine_name)
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'{MEDICINE_DATABASE[medicine_name]["name"]} added to profile'
    })

# ============================================
# REDIRECT .html FILES
# ============================================

@medicine_bp.route('/<path:filename>.html')
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