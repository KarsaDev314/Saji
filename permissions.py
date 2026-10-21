"""Aturan otorisasi. Tidak menyentuh storage. Pure logic."""
from flask_login import current_user

import config


def current_id():
    """ID user yang login sebagai int, atau None kalau anonim."""
    return int(current_user.id) if current_user.is_authenticated else None


def is_admin():
    return current_user.is_authenticated and current_user.username == config.ADMIN_USERNAME


def can_edit_recipe(recipe):
    if not current_user.is_authenticated:
        return False
    if is_admin():
        return True
    return str(recipe.get("user_id", 0)) == str(current_user.id)


def can_moderate_comment(comment, recipe):
    if not current_user.is_authenticated:
        return False
    if is_admin():
        return True
    uid = int(current_user.id)
    return recipe.get("user_id") == uid or comment.get("user_id") == uid