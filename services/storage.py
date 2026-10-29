from core.db import db
from core.db_models import User, Recipe, Follow, Favorite, RecipeLike, Comment, CommentReaction, Notification

def load_users():
    users = User.query.all()
    result = []
    for u in users:
        following = [f.followed_id for f in Follow.query.filter_by(follower_id=u.id).all()]
        favs = [f.recipe_id for f in Favorite.query.filter_by(user_id=u.id).all()]
        result.append({
            "id": u.id, 
            "username": u.username, 
            "bio": u.bio, 
            "profile_pic": u.profile_pic,
            "following": following,
            "favorit_ids": favs
        })
    return result

def find_record_by_id(user_id):
    u = db.session.get(User, int(user_id))
    if not u: return None
    following = [f.followed_id for f in Follow.query.filter_by(follower_id=u.id).all()]
    favs = [f.recipe_id for f in Favorite.query.filter_by(user_id=u.id).all()]
    return {
        "id": u.id, 
        "username": u.username, 
        "bio": u.bio, 
        "profile_pic": u.profile_pic,
        "join_date": str(u.created_at)[:10] if u.created_at else "",
        "following": following,
        "favorit_ids": favs
    }

def find_by_username(username):
    u = User.query.filter_by(username=username).first()
    if not u: return None
    return find_record_by_id(u.id)

def load_recipes():
    recipes = Recipe.query.all()
    result = []
    for r in recipes:
        result.append({
            "id": r.id,
            "nama": r.nama,
            "kategori": r.kategori,
            "waktu": r.waktu,
            "bahan": r.bahan.split("\n") if r.bahan else [],
            "langkah": r.langkah.split("\n") if r.langkah else [],
            "user_id": r.user_id,
            "rating": 0,
            "likes": [l.user_id for l in RecipeLike.query.filter_by(recipe_id=r.id).all()],
            "comments": []
        })
    return result