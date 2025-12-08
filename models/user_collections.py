"""
User Collections - Search History, Favorites, and Reviews
File: models/user_collections.py
"""

from pymongo import MongoClient, DESCENDING
from datetime import datetime
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# MONGODB CONNECTION (Same as database.py)
# ============================================

mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
database_name = os.getenv('DATABASE_NAME', 'MedInfo')

client = MongoClient(mongodb_uri)
db = client[database_name]

# ============================================
# NEW COLLECTIONS
# ============================================

search_history_collection = db['search_history']
user_favorites_collection = db['user_favorites']
user_reviews_collection = db['user_reviews']

print(f"✅ Connected to new collections: search_history, user_favorites, user_reviews")

# ============================================
# CREATE INDEXES FOR BETTER PERFORMANCE
# ============================================

# Search History indexes
search_history_collection.create_index([("user_email", 1), ("timestamp", -1)])
search_history_collection.create_index("medicine_name")

# Favorites indexes
user_favorites_collection.create_index([("user_email", 1), ("medicine_name", 1)], unique=True)

# Reviews indexes
user_reviews_collection.create_index([("user_email", 1), ("medicine_name", 1)])
user_reviews_collection.create_index("medicine_name")

# ============================================
# SEARCH HISTORY FUNCTIONS
# ============================================

def add_to_search_history(user_email, medicine_name):
    """
    Add a medicine search to user's search history.
    If already searched, update timestamp and increment count.
    
    Args:
        user_email (str): User's email
        medicine_name (str): Medicine name searched
    
    Returns:
        ObjectId: ID of the search entry
    """
    try:
        medicine_name_lower = medicine_name.lower()
        
        # Check if this medicine was already searched by this user
        existing = search_history_collection.find_one({
            'user_email': user_email,
            'medicine_name': medicine_name_lower
        })
        
        if existing:
            # Update timestamp and increment search count
            search_history_collection.update_one(
                {'_id': existing['_id']},
                {
                    '$set': {'timestamp': datetime.utcnow()},
                    '$inc': {'search_count': 1}
                }
            )
            print(f"✅ Updated search history for {user_email}: {medicine_name}")
            return existing['_id']
        else:
            # Insert new search entry
            search_entry = {
                'user_email': user_email,
                'medicine_name': medicine_name_lower,
                'timestamp': datetime.utcnow(),
                'search_count': 1
            }
            result = search_history_collection.insert_one(search_entry)
            print(f"✅ Added to search history for {user_email}: {medicine_name}")
            return result.inserted_id
    
    except Exception as e:
        print(f"❌ Error adding to search history: {e}")
        return None


def get_user_search_history(user_email, limit=10):
    """
    Get user's search history (most recent first).
    
    Args:
        user_email (str): User's email
        limit (int): Maximum number of results to return
    
    Returns:
        list: List of search history entries
    """
    try:
        history = list(search_history_collection.find(
            {'user_email': user_email}
        ).sort('timestamp', DESCENDING).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for item in history:
            item['_id'] = str(item['_id'])
        
        return history
    
    except Exception as e:
        print(f"❌ Error getting search history: {e}")
        return []


def clear_search_history(user_email):
    """
    Clear all search history for a user.
    
    Args:
        user_email (str): User's email
    
    Returns:
        int: Number of entries deleted
    """
    try:
        result = search_history_collection.delete_many({'user_email': user_email})
        print(f"✅ Cleared {result.deleted_count} search history entries for {user_email}")
        return result.deleted_count
    
    except Exception as e:
        print(f"❌ Error clearing search history: {e}")
        return 0


# ============================================
# USER FAVORITES FUNCTIONS
# ============================================

def add_to_favorites(user_email, medicine_name):
    """
    Add a medicine to user's favorites.
    
    Args:
        user_email (str): User's email
        medicine_name (str): Medicine name to add
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        favorite_entry = {
            'user_email': user_email,
            'medicine_name': medicine_name.lower(),
            'added_at': datetime.utcnow()
        }
        
        # Try to insert (will fail if already exists due to unique index)
        user_favorites_collection.insert_one(favorite_entry)
        print(f"✅ Added {medicine_name} to favorites for {user_email}")
        return True
    
    except Exception as e:
        # Duplicate key error means it's already in favorites
        if 'duplicate key' in str(e).lower():
            print(f"ℹ️ {medicine_name} already in favorites for {user_email}")
            return True
        print(f"❌ Error adding to favorites: {e}")
        return False


def remove_from_favorites(user_email, medicine_name):
    """
    Remove a medicine from user's favorites.
    
    Args:
        user_email (str): User's email
        medicine_name (str): Medicine name to remove
    
    Returns:
        bool: True if removed, False otherwise
    """
    try:
        result = user_favorites_collection.delete_one({
            'user_email': user_email,
            'medicine_name': medicine_name.lower()
        })
        
        if result.deleted_count > 0:
            print(f"✅ Removed {medicine_name} from favorites for {user_email}")
            return True
        else:
            print(f"ℹ️ {medicine_name} not in favorites for {user_email}")
            return False
    
    except Exception as e:
        print(f"❌ Error removing from favorites: {e}")
        return False


def get_user_favorites(user_email):
    """
    Get all favorites for a user.
    
    Args:
        user_email (str): User's email
    
    Returns:
        list: List of favorite medicines
    """
    try:
        favorites = list(user_favorites_collection.find(
            {'user_email': user_email}
        ).sort('added_at', DESCENDING))
        
        # Convert ObjectId to string
        for item in favorites:
            item['_id'] = str(item['_id'])
        
        return favorites
    
    except Exception as e:
        print(f"❌ Error getting favorites: {e}")
        return []


def is_favorite(user_email, medicine_name):
    """
    Check if a medicine is in user's favorites.
    
    Args:
        user_email (str): User's email
        medicine_name (str): Medicine name to check
    
    Returns:
        bool: True if in favorites, False otherwise
    """
    try:
        count = user_favorites_collection.count_documents({
            'user_email': user_email,
            'medicine_name': medicine_name.lower()
        })
        return count > 0
    
    except Exception as e:
        print(f"❌ Error checking favorite: {e}")
        return False


# ============================================
# USER REVIEWS FUNCTIONS
# ============================================

def add_review(user_email, medicine_name, rating, review_text):
    """
    Add a review for a medicine.
    
    Args:
        user_email (str): User's email
        medicine_name (str): Medicine name
        rating (int): Rating (1-5 stars)
        review_text (str): Review text
    
    Returns:
        ObjectId: ID of the review, or None if failed
    """
    try:
        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            print(f"❌ Invalid rating: {rating}. Must be 1-5")
            return None
        
        review_entry = {
            'user_email': user_email,
            'medicine_name': medicine_name.lower(),
            'rating': rating,
            'review_text': review_text,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = user_reviews_collection.insert_one(review_entry)
        print(f"✅ Added review for {medicine_name} by {user_email}")
        return result.inserted_id
    
    except Exception as e:
        print(f"❌ Error adding review: {e}")
        return None


def update_review(review_id, rating=None, review_text=None):
    """
    Update an existing review.
    
    Args:
        review_id (str): Review ID
        rating (int, optional): New rating
        review_text (str, optional): New review text
    
    Returns:
        bool: True if updated, False otherwise
    """
    try:
        update_data = {'updated_at': datetime.utcnow()}
        
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                print(f"❌ Invalid rating: {rating}")
                return False
            update_data['rating'] = rating
        
        if review_text is not None:
            update_data['review_text'] = review_text
        
        result = user_reviews_collection.update_one(
            {'_id': ObjectId(review_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            print(f"✅ Updated review {review_id}")
            return True
        else:
            print(f"ℹ️ No changes made to review {review_id}")
            return False
    
    except Exception as e:
        print(f"❌ Error updating review: {e}")
        return False


def delete_review(review_id):
    """
    Delete a review.
    
    Args:
        review_id (str): Review ID
    
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        result = user_reviews_collection.delete_one({'_id': ObjectId(review_id)})
        
        if result.deleted_count > 0:
            print(f"✅ Deleted review {review_id}")
            return True
        else:
            print(f"ℹ️ Review {review_id} not found")
            return False
    
    except Exception as e:
        print(f"❌ Error deleting review: {e}")
        return False


def get_medicine_reviews(medicine_name):
    """
    Get all reviews for a specific medicine.
    
    Args:
        medicine_name (str): Medicine name
    
    Returns:
        list: List of reviews
    """
    try:
        reviews = list(user_reviews_collection.find(
            {'medicine_name': medicine_name.lower()}
        ).sort('created_at', DESCENDING))
        
        # Convert ObjectId to string
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return reviews
    
    except Exception as e:
        print(f"❌ Error getting reviews: {e}")
        return []


def get_user_reviews(user_email):
    """
    Get all reviews by a specific user.
    
    Args:
        user_email (str): User's email
    
    Returns:
        list: List of user's reviews
    """
    try:
        reviews = list(user_reviews_collection.find(
            {'user_email': user_email}
        ).sort('created_at', DESCENDING))
        
        # Convert ObjectId to string
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return reviews
    
    except Exception as e:
        print(f"❌ Error getting user reviews: {e}")
        return []


def get_medicine_average_rating(medicine_name):
    """
    Calculate average rating for a medicine.
    
    Args:
        medicine_name (str): Medicine name
    
    Returns:
        dict: {'average': float, 'count': int} or None if no reviews
    """
    try:
        pipeline = [
            {'$match': {'medicine_name': medicine_name.lower()}},
            {'$group': {
                '_id': None,
                'average_rating': {'$avg': '$rating'},
                'review_count': {'$sum': 1}
            }}
        ]
        
        result = list(user_reviews_collection.aggregate(pipeline))
        
        if result:
            return {
                'average': round(result[0]['average_rating'], 1),
                'count': result[0]['review_count']
            }
        else:
            return None
    
    except Exception as e:
        print(f"❌ Error calculating average rating: {e}")
        return None