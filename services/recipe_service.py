from core.db import db
from core.db_models import Recipe, User, RecipeLike, Favorite, Comment, CommentReaction
from flask_login import current_user
from services import storage

def all():
    return storage.load_recipes()

def find(recipe_id):
    r = Recipe.query.get(int(recipe_id))
    if not r: return None
    likes = [l.user_id for l in RecipeLike.query.filter_by(recipe_id=r.id).all()]
    return {
        "id": r.id, "nama": r.nama, "kategori": r.kategori, "waktu": r.waktu, 
        "bahan": r.bahan.split("\n") if r.bahan else [], 
        "langkah": r.langkah.split("\n") if r.langkah else [], 
        "user_id": r.user_id, "rating": r.rating, "catatan": r.catatan, "likes": likes
    }

def create(data):
    new_r = Recipe(
        nama=data['nama'], kategori=data['kategori'], waktu=data['waktu'],
        bahan="\n".join(data['bahan']), langkah="\n".join(data['langkah']),
        user_id=int(current_user.id)
    )
    db.session.add(new_r)
    db.session.commit()
    return new_r.id

def update(recipe_id, data):
    r = Recipe.query.get(int(recipe_id))
    if r:
        r.nama = data['nama']
        r.kategori = data['kategori']
        r.waktu = data['waktu']
        r.bahan = "\n".join(data['bahan'])
        r.langkah = "\n".join(data['langkah'])
        db.session.commit()

def delete(recipe_id):
    r = Recipe.query.get(int(recipe_id))
    if r:
        RecipeLike.query.filter_by(recipe_id=r.id).delete()
        Favorite.query.filter_by(recipe_id=r.id).delete()
        comments = Comment.query.filter_by(recipe_id=r.id).all()
        for c in comments:
            CommentReaction.query.filter_by(comment_id=c.id).delete()
        Comment.query.filter_by(recipe_id=r.id).delete()
        db.session.delete(r)
        db.session.commit()

def toggle_like(recipe_id):
    existing = RecipeLike.query.filter_by(user_id=int(current_user.id), recipe_id=recipe_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(RecipeLike(user_id=int(current_user.id), recipe_id=recipe_id))
    db.session.commit()

def set_rating(recipe_id, rating, catatan):
    r = Recipe.query.get(int(recipe_id))
    if r:
        r.rating = rating
        r.catatan = catatan
        db.session.commit()

def toggle_favorite(recipe_id):
    existing = Favorite.query.filter_by(user_id=int(current_user.id), recipe_id=recipe_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Favorite(user_id=int(current_user.id), recipe_id=recipe_id))
    db.session.commit()

def owner_public(recipe):
    u = User.query.get(recipe.get("user_id"))
    return {"id": u.id, "username": u.username, "bio": u.bio, "profile_pic": u.profile_pic} if u else None

def filter_(recipes, keyword, kategori, only_favorite, favorite_ids):
    result = recipes
    if kategori:
        result = [r for r in result if r.get("kategori") == kategori]
    if only_favorite:
        result = [r for r in result if r["id"] in favorite_ids]
    if keyword:
        kw = keyword.lower()
        result = [
            r for r in result
            if kw in r["nama"].lower() or any(kw in b.lower() for b in r.get("bahan", []))
        ]
    return result

def feed(users, recipes, user_id):
    following = next((u.get("following", []) for u in users if u["id"] == user_id), [])
    relevant = set(following) | {user_id, 0}
    return [r for r in recipes if r.get("user_id") in relevant]

def by_owner(recipes, user_id):
    return [r for r in recipes if r.get("user_id") == user_id]

def is_favorite(recipe_id):
    return Favorite.query.filter_by(user_id=int(current_user.id), recipe_id=recipe_id).first() is not None