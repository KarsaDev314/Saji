"""Skema database SQLAlchemy. Sumber tunggal kebenaran untuk struktur tabel."""
from flask_login import UserMixin

from db import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(300), default="")
    join_date = db.Column(db.String(20), default="")

    def to_public_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio or "",
            "join_date": self.join_date or "",
        }


class Follow(db.Model):
    """Tabel relasi follow: siapa follow siapa."""
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(30))
    waktu = db.Column(db.String(50))
    bahan = db.Column(db.JSON, default=list)      # array of string
    langkah = db.Column(db.JSON, default=list)    # array of string
    rating = db.Column(db.Integer, default=0)
    catatan = db.Column(db.String(1000), default="")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default=0, nullable=False, index=True)


class Favorite(db.Model):
    """User memfavoritkan resep tertentu."""
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)


class RecipeLike(db.Model):
    """User menyukai resep tertentu."""
    __tablename__ = "recipe_likes"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.String(8), primary_key=True)  # uuid[:8] sesuai kode lama
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    username = db.Column(db.String(30))
    teks = db.Column(db.String(500), nullable=False)
    waktu = db.Column(db.String(20))
    parent_id = db.Column(db.String(8), db.ForeignKey("comments.id"), nullable=True)


class CommentReaction(db.Model):
    """Like/dislike untuk komentar. type: 'like' atau 'dislike'."""
    __tablename__ = "comment_reactions"
    comment_id = db.Column(db.String(8), db.ForeignKey("comments.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    type = db.Column(db.String(10), primary_key=True)


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.String(8), primary_key=True)
    penerima_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    pengirim_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pengirim_username = db.Column(db.String(30))
    tipe = db.Column(db.String(20))
    pesan = db.Column(db.String(500))
    tautan = db.Column(db.String(200))
    waktu = db.Column(db.String(20))
    dibaca = db.Column(db.Boolean, default=False)