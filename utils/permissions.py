from flask_login import current_user
import config

def current_id():
    return int(current_user.id) if current_user.is_authenticated else None

def can_edit_recipe(recipe):
    if not current_user.is_authenticated: return False
    if current_user.username == "admin": return True
    return str(recipe.get("user_id", 0)) == str(current_user.id)

def can_moderate_comment(comment, recipe):
    if not current_user.is_authenticated: 
        return False
    if current_user.username == "admin": 
        return True
        
    uid = int(current_user.id)
    # Handle kalau comment berupa objek SQLAlchemy atau dictionary
    c_user_id = comment.user_id if hasattr(comment, 'user_id') else comment.get("user_id")
    
    return recipe.get("user_id") == uid or c_user_id == uid