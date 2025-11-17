"""
Database Models - In-memory storage with JSON persistence
File: models/database.py
"""

import json
import os

# ============================================
# USERS DATABASE
# ============================================

USERS_DATABASE = {}

# ============================================
# MEDICINE DATABASE WITH JSON PERSISTENCE
# ============================================

# Path to save medicines
MEDICINE_DB_FILE = 'medicine_database.json'

# Default medicines (always available)
DEFAULT_MEDICINES = {
    'aspirin': {
        'name': 'Aspirin',
        'description': 'Aspirin is a common painkiller that helps reduce pain, fever, and inflammation in your body. It works by blocking chemicals that cause pain and swelling. Doctors also prescribe it to prevent heart attacks and strokes because it stops blood from clotting too much. You can buy it at any pharmacy without a prescription.',
        'advice': '• Take with food or a full glass of water\n• Don\'t take on an empty stomach\n• Take one tablet every 4-6 hours as needed\n• Don\'t take more than 8 tablets in 24 hours',
        'warning': '• Don\'t mix with other painkillers without asking a doctor\n• Avoid if you have stomach ulcers or bleeding problems\n• Don\'t drink alcohol while taking it\n• May cause stomach upset or bleeding in some people',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=aspirin'
    },
    'ibuprofen': {
        'name': 'Ibuprofen',
        'description': 'Ibuprofen is a painkiller that helps with headaches, muscle aches, period pain, and fever. It belongs to a group of medicines called NSAIDs which reduce inflammation and pain in your body. It works by blocking chemicals that cause swelling and pain. You can buy it at pharmacies without a prescription for short-term use.',
        'advice': '• Take with food or milk to protect your stomach\n• Drink plenty of water with each dose\n• Take the lowest dose that works for you\n• Don\'t use for more than 10 days without seeing a doctor',
        'warning': '• Don\'t take if you have stomach problems or asthma\n• May increase risk of heart problems if used long-term\n• Avoid alcohol while taking this medicine\n• Can interact badly with blood pressure medicines',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=ibuprofen'
    },
    'paracetamol': {
        'name': 'Paracetamol',
        'description': 'Paracetamol (also called acetaminophen) is a very common medicine for pain and fever. It helps with headaches, toothaches, period pain, cold symptoms, and reducing high temperature. It\'s gentler on your stomach than other painkillers and is safe for most people when used correctly. You can buy it without a prescription.',
        'advice': '• Can take with or without food\n• Take one or two tablets every 4-6 hours as needed\n• Wait at least 4 hours between doses\n• Read the label carefully - many cold medicines also contain paracetamol',
        'warning': '• Never take more than 8 tablets (4000mg) in 24 hours\n• Taking too much can cause serious liver damage\n• Don\'t drink alcohol while taking this\n• Check other medicines don\'t also contain paracetamol',
        'pubmed_link': 'https://pubmed.ncbi.nlm.nih.gov/?term=paracetamol'
    }
}

def load_medicine_database():
    """Load medicines from JSON file"""
    # Start with default medicines
    medicines = DEFAULT_MEDICINES.copy()
    
    # Load AI-generated medicines from file if exists
    if os.path.exists(MEDICINE_DB_FILE):
        try:
            with open(MEDICINE_DB_FILE, 'r', encoding='utf-8') as f:
                saved_medicines = json.load(f)
                # Merge with defaults (defaults take priority)
                for key, value in saved_medicines.items():
                    if key not in medicines:
                        medicines[key] = value
                print(f"✓ Loaded {len(saved_medicines)} medicines from {MEDICINE_DB_FILE}")
        except Exception as e:
            print(f"Error loading medicine database: {e}")
    
    return medicines

def save_medicine_to_file(medicine_name, medicine_data):
    """Save a new medicine to JSON file"""
    try:
        # Load existing medicines from file
        existing_medicines = {}
        if os.path.exists(MEDICINE_DB_FILE):
            with open(MEDICINE_DB_FILE, 'r', encoding='utf-8') as f:
                existing_medicines = json.load(f)
        
        # Add new medicine
        existing_medicines[medicine_name] = medicine_data
        
        # Save back to file
        with open(MEDICINE_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_medicines, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved '{medicine_name}' to {MEDICINE_DB_FILE}")
        return True
    except Exception as e:
        print(f"Error saving medicine to file: {e}")
        return False

# Load medicines on startup
MEDICINE_DATABASE = load_medicine_database()

# ============================================
# PASSWORD RESET TOKENS
# ============================================

RESET_TOKENS = {
    # Example:
    # 'token_string': {
    #     'email': 'user@example.com',
    #     'expires': datetime_object
    # }
}