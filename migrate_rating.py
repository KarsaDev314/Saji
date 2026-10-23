from app import app
from db import db
import storage
from db_models import User, Follow, Recipe, Favorite, RecipeLike, Comment, CommentReaction, Notification, RecipeRating
import json
import os

def load_json(path):
    if not os.path.exists(path): return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data[list(data.keys())[0]]

def migrate():
    with app.app_context():
        print("Menghapus tabel lama...")
        db.drop_all()
        db.create_all()

        users_data = load_json("_archive/users.json")
        recipes_data = load_json("_archive/resep.json")
        notifs_data = load_json("_archive/notifikasi.json")

        print("Migrasi Users...")
        for u in users_data:
            user = User(id=u["id"], username=u["username"], password_hash=u["password_hash"], bio=u.get("bio", ""), join_date=u.get("join_date", ""))
            db.session.add(user)
            for fid in u.get("following", []): db.session.add(Follow(follower_id=u["id"], following_id=fid))
            for rid in u.get("favorit_ids", []): db.session.add(Favorite(user_id=u["id"], recipe_id=rid))

        print("Migrasi Recipes & Komentar...")
        for r in recipes_data:
            recipe = Recipe(id=r["id"], nama=r["nama"], kategori=r.get("kategori", ""), waktu=r.get("waktu", "-"), bahan=r.get("bahan", []), langkah=r.get("langkah", []), user_id=r.get("user_id", 0))
            db.session.add(recipe)
            
            for uid in r.get("likes", []): db.session.add(RecipeLike(user_id=uid, recipe_id=r["id"]))

            # Fungsi flatten komentar (sama kayak sebelumnya)
            def flatten(comments, rid, pid=None):
                res = []
                for c in comments:
                    res.append((c, rid, pid))
                    if c.get("replies"): res.extend(flatten(c["replies"], rid, c["id"]))
                return res

            for c, rid, pid in flatten(r.get("comments", []), r["id"]):
                db.session.add(Comment(id=c["id"], recipe_id=rid, user_id=c["user_id"], username=c.get("username", ""), teks=c["teks"], waktu=c.get("waktu", ""), parent_id=pid))
                for uid in c.get("likes", []): db.session.add(CommentReaction(comment_id=c["id"], user_id=uid, type="like"))
                for uid in c.get("dislikes", []): db.session.add(CommentReaction(comment_id=c["id"], user_id=uid, type="dislike"))

        print("Migrasi Notifikasi...")
        for n in notifs_data:
            db.session.add(Notification(id=n["id"], penerima_id=n["penerima_id"], pengirim_id=n.get("pengirim_id"), pengirim_username=n.get("pengirim_username"), tipe=n.get("tipe"), pesan=n.get("pesan"), tautan=n.get("tautan"), waktu=n.get("waktu"), dibaca=n.get("dibaca", False)))

        db.session.commit()
        print("=== MIGRASI BERHASIL ===")

if __name__ == "__main__":
    migrate()