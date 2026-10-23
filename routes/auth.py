from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from core.db import db
from core.db_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from utils import validators

def register(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(username=request.form.get("username")).first()
            if user and check_password_hash(user.password_hash, request.form.get("password")):
                login_user(user)
                return redirect(url_for("index"))
            flash("Login gagal", "info")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            u = request.form.get("username").strip()
            p = request.form.get("password")
            err = validators.validate_username_format(u)
            if err: 
                flash(err, "info")
            else:
                db.session.add(User(username=u, password_hash=generate_password_hash(p)))
                db.session.commit()
                return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        logout_user()
        return redirect(url_for("index"))