from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from extensions import limiter
import config
from services import user_service  # <-- Ada from services
from utils import validators       # <-- Ada from utils

def register(app):
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            password2 = request.form.get("password2", "")
            error = validators.validate_registration(username, password, password2)
            if not error and user_service.find_by_username(username):
                error = "Username sudah dipakai. Coba yang lain."
            if error:
                return render_template("register.html", error=error), 400
            user = user_service.register(username, password)
            login_user(user)
            flash(f"Selamat datang, {username}! Akun berhasil dibuat.", config.FLASH_SUKSES)
            return redirect(url_for("index"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    @limiter.limit("5 per minute")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = user_service.authenticate(username, password)
            if not user:
                return render_template("login.html", error="Username atau password salah."), 400
            login_user(user)
            flash(f"Halo, {username}! Kamu berhasil login.", config.FLASH_SUKSES)
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("index"))
        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("Kamu sudah logout.", config.FLASH_INFO)
        return redirect(url_for("index"))