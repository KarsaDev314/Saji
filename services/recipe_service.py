from core.db import db
from core.db_models import Recipe, User
from services import storage

def all():
    return storage.load_recipes()

def find(recipe_id):
    r = Recipe.query.get(int(recipe_id))
    if not r: return None
    return {
        "id": r.id, 
        "nama": r.nama, 
        "kategori": r.kategori, 
        "waktu": r.waktu, 
        "bahan": r.bahan.split("\n") if r.bahan else [], 
        "langkah": r.langkah.split("\n") if r.langkah else [], 
        "user_id": r.user_id
    }

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
            if kw in r["nama"].lower()
            or any(kw in b.lower() for b in r.get("bahan", []))
        ]
    return result

def feed(users, recipes, user_id):
    following = next((u.get("following", []) for u in users if u["id"] == user_id), [])
    relevant = set(following) | {user_id, 0}
    return [r for r in recipes if r.get("user_id") in relevant]

def by_owner(recipes, user_id):
    return [r for r in recipes if r.get("user_id") == user_id]