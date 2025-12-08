"""
Security utilities for password hashing and JWT tokens
File: utils/security.py
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Get secret key from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# ============================================
# PASSWORD HASHING WITH BCRYPT
# ============================================

def hash_password(password):
    """
    Hash a password using bcrypt with salt
    
    Args:
        password (str): Plain text password
    
    Returns:
        str: Hashed password
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Verify a password against its hash
    
    Args:
        password (str): Plain text password
        hashed_password (str): Hashed password from database
    
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


# ============================================
# JWT TOKEN GENERATION
# ============================================

def generate_token(user_email):
    """
    Generate a JWT token for a user
    
    Args:
        user_email (str): User's email address
    
    Returns:
        str: JWT token
    """
    payload = {
        'email': user_email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token):
    """
    Verify and decode a JWT token
    
    Args:
        token (str): JWT token
    
    Returns:
        dict: Decoded payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


# ============================================
# PASSWORD VALIDATION
# ============================================

def validate_password_strength(password):
    """
    Validate password meets minimum requirements
    
    Args:
        password (str): Password to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    return True, "Password is valid"