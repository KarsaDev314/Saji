from flask_login import current_user
import config

def current_id():
    return int(current_user.id) if current_user.is_authenticated else None

def can_edit_recipe(recipe):
    if not current_user.is_authenticated: return False
    if current_user.username == "admin": return True
    return str(recipe.get("user_id", 0)) == str(current_user.id)

def can_moderate_comment(comment, recipe):
    if not current_user.is_authenticated: return False
    if current_user.username == "admin": return True
    return recipe.get("user_id") == int(current_user.id) or comment.get("user_id") == int(current_user.id)