"""
Database Models - In-memory storage
File: models/database.py
"""

# ============================================
# USERS DATABASE
# ============================================

USERS_DATABASE = {}

# Example structure:
# USERS_DATABASE = {
#     'user@email.com': {
#         'user_id': 1,
#         'fullname': 'John Doe',
#         'email': 'user@email.com',
#         'password': 'hashed_password_here'
#     }
# }

# ============================================
# MEDICINE DATABASE
# ============================================

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
# PASSWORD RESET TOKENS
# ============================================

RESET_TOKENS = {
    # Example:
    # 'token_string': {
    #     'email': 'user@example.com',
    #     'expires': datetime_object
    # }
}