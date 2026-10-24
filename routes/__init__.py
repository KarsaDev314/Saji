from routes import auth, main, recipes, comments, users, notifications, bugs

def register_all(app):
    auth.register(app)
    main.register(app)
    recipes.register(app)
    comments.register(app)
    users.register(app)
    notifications.register(app)
    bugs.register(app) # <--- Ini yang bikin route-nya kedaftar