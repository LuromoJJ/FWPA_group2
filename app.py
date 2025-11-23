"""
Flask Application Entry Point
File: app.py
"""

from flask import Flask
import os

# ============================================
# FLASK APP INITIALIZATION
# ============================================

def create_app():
    """Factory function to create Flask app"""
    
    # Get absolute paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    
    # Initialize Flask
    app = Flask(__name__, 
                template_folder=TEMPLATE_DIR,
                static_folder=STATIC_DIR)
    
    app.secret_key = 'key123'  # Change this in production!
    
    # Debug: Print paths
    print(f"Template folder: {TEMPLATE_DIR}")
    print(f"Static folder: {STATIC_DIR}")
    
    # ============================================
    # REGISTER BLUEPRINTS (Routes)
    # ============================================
    
    from routes.auth_routes import auth_bp
    from routes.medicine_routes import medicine_bp
    from routes.profile_routes import profile_bp
    from routes.form_routes import form_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(medicine_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(form_bp)
    
    # ============================================
    # ERROR HANDLERS
    # ============================================
    
    @app.errorhandler(404)
    def not_found(e):
        from flask import jsonify
        return jsonify({'error': 'Page not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        from flask import jsonify
        return jsonify({'error': 'Server error'}), 500
    
    return app

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    app = create_app()
    
    print("\n=== Starting Flask Server ===")
    print("Homepage: http://localhost:5000/")
    print("Signup: http://localhost:5000/signup")
    print("Login: http://localhost:5000/login")
    print("Medicine: http://localhost:5000/medicine/aspirin")
    print("Profile: http://localhost:5000/profile_page")
    print("Form: http://localhost:5000/form")
    print("Forgot Password: http://localhost:5000/forgot_password")
    print("Set new Password: http://localhost:5000/set_new_password/<token>")
    print("\nPress CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)