"""Registrasi semua route ke app."""
from routes import auth, comments, main, notifications, recipes, users


def register_all(app):
    auth.register(app)
    main.register(app)
    recipes.register(app)
    comments.register(app)
    users.register(app)
    notifications.register(app)