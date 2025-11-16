"""
Helper Functions and Utilities
File: utils/helpers.py
"""

from flask import session
from models.database import RESET_TOKENS, USERS_DATABASE
from datetime import datetime

# ============================================
# USER SESSION HELPERS
# ============================================

def get_current_user():
    """Check if user is logged in and return user info"""
    if 'user_id' in session:
        return {
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'email': session.get('email')
        }
    return {'logged_in': False}

# ============================================
# PASSWORD RESET TOKEN HELPERS
# ============================================

def validate_reset_token(token):
    """Check if reset token is valid and not expired"""
    token_data = RESET_TOKENS.get(token)
    if not token_data:
        return None
    
    # Check if token is expired
    expires = token_data.get('expires')
    if expires and datetime.now() > expires:
        # Token expired, remove it
        del RESET_TOKENS[token]
        return None
    
    # Token is valid, return associated email
    return token_data.get('email')

def invalidate_reset_token(token):
    """Remove token after use"""
    if token in RESET_TOKENS:
        del RESET_TOKENS[token]

# ============================================
# USER DATABASE HELPERS
# ============================================

def update_user_password(email, new_password):
    """Update user password in database"""
    if email in USERS_DATABASE:
        USERS_DATABASE[email]["password"] = new_password
        return True
    return False