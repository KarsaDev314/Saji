from datetime import datetime, timezone
from flask_login import UserMixin
from core.db import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # Username sering dipakai buat login & profil, wajib di-index
    username = db.Column(db.String(80), unique=True, nullable=False, index=True) 
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default="")
    profile_pic = db.Column(db.String(255), default="default_avatar.png")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    # Kategori sering dipakai buat filter di beranda
    kategori = db.Column(db.String(50), nullable=False, index=True) 
    waktu = db.Column(db.String(50), nullable=False)
    bahan = db.Column(db.Text, nullable=False)
    langkah = db.Column(db.Text, nullable=False)
    # User_id dipakai buat Feed dan Profil
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Integer, default=0)
    catatan = db.Column(db.String(255), default="")


class Follow(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True)
    # Sering dipanggil buat ngitung follower/following
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False, index=True)

class RecipeLike(db.Model):
    __tablename__ = "recipe_likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False, index=True)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    # Sering dipanggil buat nampilin komentar di detail resep
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class CommentReaction(db.Model):
    __tablename__ = "comment_reactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False, index=True)
    is_like = db.Column(db.Boolean, default=True)

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class BugReport(db.Model):
    __tablename__ = "bug_reports"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    message = db.Column(db.Text, nullable=False)
    # Admin sering filter berdasarkan status 'pending'
    status = db.Column(db.String(20), default="pending", index=True) 
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))