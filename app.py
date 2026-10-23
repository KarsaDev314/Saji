import os
from flask import Flask, render_template
from flask_login import current_user
import config
from extensions import csrf, login_manager
from core.db import db
from services import notification_service
from services.user_service import find_by_id
from routes import register_all

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "saji.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Tambahan buat testing
    if test_config:
        app.config.update(test_config)
        
    db.init_app(app)

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Silakan login dulu untuk mengakses halaman ini."
    login_manager.login_message_category = "info"

    register_all(app)
    _register_error_handlers(app)
    _register_context_processors(app)
    _register_security_headers(app)

    with app.app_context():
        from core.db_models import User, Recipe, Follow, Favorite, RecipeLike, Comment, CommentReaction, Notification
        db.create_all()

    return app

def _register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("404.html", kode=403, pesan="Kamu tidak punya izin."), 403
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404
    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("404.html", kode=500), 500

def _register_context_processors(app):
    @app.context_processor
    def inject_unread_notif():
        if not current_user.is_authenticated:
            return {"unread_notif": 0}
        return {"unread_notif": notification_service.unread_count(int(current_user.id))}

def _register_security_headers(app):
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

@login_manager.user_loader
def load_user(user_id):
    return find_by_id(user_id)

app = create_app()

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, host=config.HOST, port=config.PORT)