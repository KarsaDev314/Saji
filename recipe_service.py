"""Operasi bisnis resep."""
from flask_login import current_user

import config
import notification_service
import storage
import user_service
from models import to_public_dict
from db import db
from db_models import RecipeRating, RecipeLike, Favorite, Comment, CommentReaction


def all():
    recipes = storage.load_recipes()
    if current_user.is_authenticated:
        user_ratings = {rr.recipe_id: rr for rr in RecipeRating.query.filter_by(user_id=int(current_user.id)).all()}
        for r in recipes:
            rr = user_ratings.get(r["id"])
            r["rating"] = rr.rating if rr else 0
            r["catatan"] = rr.catatan if rr else ""
    return recipes


def find(recipe_id):
    recipes = storage.load_recipes()
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe is None: 
        return None
    
    if current_user.is_authenticated:
        rr = RecipeRating.query.filter_by(user_id=int(current_user.id), recipe_id=recipe_id).first()
        recipe["rating"] = rr.rating if rr else 0
        recipe["catatan"] = rr.catatan if rr else ""
    else:
        recipe["rating"] = 0
        recipe["catatan"] = ""
    return recipe


def create(data):
    recipes = storage.load_recipes()
    new_id = max((r["id"] for r in recipes), default=0) + 1
    record = {
        "id": new_id,
        "favorit": False,
        "likes": [], "comments": [],
        "user_id": int(current_user.id),
        **data,
    }
    recipes.append(record)
    storage.save_recipes(recipes)
    return new_id


def update(recipe_id, data):
    recipes = storage.load_recipes()
    for r in recipes:
        if r["id"] == recipe_id:
            r.update(data)
            break
    storage.save_recipes(recipes)


def delete(recipe_id):
    # Hapus rating-nya dulu biar gak error Foreign Key
    db.session.query(RecipeRating).filter_by(recipe_id=recipe_id).delete()
    
    recipes = [r for r in storage.load_recipes() if r["id"] != recipe_id]
    storage.save_recipes(recipes)


def toggle_like(recipe_id):
    recipes = storage.load_recipes()
    uid = int(current_user.id)
    for r in recipes:
        if r["id"] != recipe_id:
            continue
        likes = r.setdefault("likes", [])
        if uid in likes:
            likes.remove(uid)
        else:
            likes.append(uid)
            if r.get("user_id", 0) != 0:
                notification_service.send(
                    r["user_id"], uid, config.NOTIF_LIKE,
                    f"menyukai resepmu '{r['nama']}'",
                    f"/resep/{recipe_id}",
                )
        break
    storage.save_recipes(recipes)


def set_rating(recipe_id, rating, catatan):
    if not current_user.is_authenticated: 
        return
    uid = int(current_user.id)
    
    rr = db.session.get(RecipeRating, (uid, recipe_id))
    if not rr:
        rr = RecipeRating(user_id=uid, recipe_id=recipe_id)
        db.session.add(rr)
    rr.rating = rating
    rr.catatan = catatan
    db.session.commit()


def toggle_favorite(recipe_id):
    users = storage.load_users()
    uid = int(current_user.id)
    for u in users:
        if u["id"] == uid:
            favs = u.setdefault("favorit_ids", [])
            if recipe_id in favs:
                favs.remove(recipe_id)
            else:
                favs.append(recipe_id)
            break
    storage.save_users(users)


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
    following = next(
        (u.get("following", []) for u in users if u["id"] == user_id), []
    )
    relevant = set(following) | {user_id, 0}
    return [r for r in recipes if r.get("user_id") in relevant]


def by_owner(recipes, user_id):
    return [r for r in recipes if r.get("user_id") == user_id]


def owner_public(recipe):
    owner_id = recipe.get("user_id", 0)
    if not owner_id:
        return None
    record = user_service.find_record_by_id(owner_id)
    return to_public_dict(record) if record else None


def is_favorite(recipe_id):
    record = user_service.current_record()
    return bool(record and recipe_id in record.get("favorit_ids", []))