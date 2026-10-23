def register_all(app):
    from routes import auth, main, recipes, comments, users, notifications
    auth.register(app)
    main.register(app)
    recipes.register(app)
    comments.register(app)
    users.register(app)
    notifications.register(app)