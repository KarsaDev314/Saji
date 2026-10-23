"""Storage layer. Baca/tulis ke SQLite, tapi output tetap dict agar kompatibel dengan service lama."""
import json
import config
from db import db
from db_models import (
    User, Follow, Recipe, Favorite, RecipeLike,
    Comment, CommentReaction, Notification
)

# ===== USERS =====

def load_users():
    users = User.query.all()
    result = []
    for u in users:
        following = [f.following_id for f in Follow.query.filter_by(follower_id=u.id).all()]
        favorit_ids = [f.recipe_id for f in Favorite.query.filter_by(user_id=u.id).all()]
        result.append({
            "id": u.id,
            "username": u.username,
            "password_hash": u.password_hash,
            "bio": u.bio or "",
            "join_date": u.join_date or "",
            "following": following,
            "favorit_ids": favorit_ids
        })
    return result

def save_users(users_data):
    user_ids = [u["id"] for u in users_data]
    
    # Hapus user yang tidak ada di list
    User.query.filter(~User.id.in_(user_ids)).delete(synchronize_session=False)
    
    for u_data in users_data:
        user = db.session.get(User, u_data["id"])
        if not user:
            user = User(id=u_data["id"])
            db.session.add(user)
        user.username = u_data["username"]
        user.password_hash = u_data["password_hash"]
        user.bio = u_data.get("bio", "")
        user.join_date = u_data.get("join_date", "")
        
        # Sync Follows
        db.session.query(Follow).filter_by(follower_id=user.id).delete()
        for fid in u_data.get("following", []):
            db.session.add(Follow(follower_id=user.id, following_id=fid))
            
        # Sync Favorites
        db.session.query(Favorite).filter_by(user_id=user.id).delete()
        for rid in u_data.get("favorit_ids", []):
            db.session.add(Favorite(user_id=user.id, recipe_id=rid))
            
    db.session.commit()

# ===== RECIPES =====

def load_recipes():
    recipes = Recipe.query.all()
    result = []
    for r in recipes:
        likes = [l.user_id for l in RecipeLike.query.filter_by(recipe_id=r.id).all()]
        
        comments_db = Comment.query.filter_by(recipe_id=r.id).all()
        comments_tree = _build_comment_tree(comments_db)
        
        result.append({
            "id": r.id,
            "nama": r.nama,
            "kategori": r.kategori or "",
            "waktu": r.waktu or "-",
            "bahan": r.bahan or [],
            "langkah": r.langkah or [],
            "user_id": r.user_id,
            "likes": likes,
            "comments": comments_tree
        })
    return result

def _build_comment_tree(comments_db):
    comment_dict = {}
    for c in comments_db:
        likes = [r.user_id for r in CommentReaction.query.filter_by(comment_id=c.id, type="like").all()]
        dislikes = [r.user_id for r in CommentReaction.query.filter_by(comment_id=c.id, type="dislike").all()]
        comment_dict[c.id] = {
            "id": c.id, "user_id": c.user_id, "username": c.username,
            "teks": c.teks, "waktu": c.waktu, "likes": likes,
            "dislikes": dislikes, "replies": []
        }
    
    root_comments = []
    for c in comments_db:
        if c.parent_id and c.parent_id in comment_dict:
            comment_dict[c.parent_id]["replies"].append(comment_dict[c.id])
        else:
            root_comments.append(comment_dict[c.id])
    return root_comments

def save_recipes(recipes_data):
    recipe_ids = [r["id"] for r in recipes_data]
    Recipe.query.filter(~Recipe.id.in_(recipe_ids)).delete(synchronize_session=False)
    
    for r_data in recipes_data:
        recipe = db.session.get(Recipe, r_data["id"])
        if not recipe:
            recipe = Recipe(id=r_data["id"])
            db.session.add(recipe)
            
        recipe.nama = r_data["nama"]
        recipe.kategori = r_data.get("kategori", "")
        recipe.waktu = r_data.get("waktu", "-")
        recipe.bahan = r_data.get("bahan", [])
        recipe.langkah = r_data.get("langkah", [])
        recipe.user_id = r_data.get("user_id", 0)
        
        # 1. Sync Likes Resep
        db.session.query(RecipeLike).filter_by(recipe_id=recipe.id).delete()
        for uid in r_data.get("likes", []):
            db.session.add(RecipeLike(user_id=uid, recipe_id=recipe.id))
            
        # 2. HAPUS REAKSI KOMENTAR DULU (BIAR GAK ERROR UNIQUE CONSTRAINT)
        existing_comments = Comment.query.filter_by(recipe_id=recipe.id).all()
        comment_ids = [c.id for c in existing_comments]
        if comment_ids:
            db.session.query(CommentReaction).filter(CommentReaction.comment_id.in_(comment_ids)).delete(synchronize_session=False)
            
        # 3. Baru Hapus Komentarnya
        db.session.query(Comment).filter_by(recipe_id=recipe.id).delete()
        
        # 4. Masukin Ulang Komentar Baru beserta Reaksinya
        flat_comments = _flatten_comments_for_save(r_data.get("comments", []))
        for c_data in flat_comments:
            db.session.add(Comment(
                id=c_data["id"], recipe_id=recipe.id, user_id=c_data["user_id"],
                username=c_data.get("username", ""), teks=c_data["teks"],
                waktu=c_data.get("waktu", ""), parent_id=c_data.get("parent_id")
            ))
            # Masukin Like/Dislike komentar
            for uid in c_data.get("likes", []):
                db.session.add(CommentReaction(comment_id=c_data["id"], user_id=uid, type="like"))
            for uid in c_data.get("dislikes", []):
                db.session.add(CommentReaction(comment_id=c_data["id"], user_id=uid, type="dislike"))
                
    db.session.commit()

def _flatten_comments_for_save(comments, parent_id=None):
    res = []
    for c in comments:
        c_copy = c.copy()
        c_copy["parent_id"] = parent_id
        res.append(c_copy)
        if c.get("replies"):
            res.extend(_flatten_comments_for_save(c["replies"], c["id"]))
    return res

# ===== NOTIFICATIONS =====

def load_notifications():
    notifs = Notification.query.all()
    return [{
        "id": n.id, "penerima_id": n.penerima_id, "pengirim_id": n.pengirim_id,
        "pengirim_username": n.pengirim_username, "tipe": n.tipe,
        "pesan": n.pesan, "tautan": n.tautan, "waktu": n.waktu, "dibaca": n.dibaca
    } for n in notifs]

def save_notifications(notifs_data):
    notif_ids = [n["id"] for n in notifs_data]
    Notification.query.filter(~Notification.id.in_(notif_ids)).delete(synchronize_session=False)
    
    for n_data in notifs_data:
        notif = db.session.get(Notification, n_data["id"])
        if not notif:
            notif = Notification(id=n_data["id"])
            db.session.add(notif)
        notif.penerima_id = n_data["penerima_id"]
        notif.pengirim_id = n_data.get("pengirim_id")
        notif.pengirim_username = n_data.get("pengirim_username")
        notif.tipe = n_data.get("tipe")
        notif.pesan = n_data.get("pesan")
        notif.tautan = n_data.get("tautan")
        notif.waktu = n_data.get("waktu")
        notif.dibaca = n_data.get("dibaca", False)
        
    db.session.commit()