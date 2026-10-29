from werkzeug.security import generate_password_hash, check_password_hash
from services import storage
from core.db import db
from core.db_models import User, Follow

def all():
    return storage.load_users()

def find_by_id(user_id):
    return db.session.get(User, int(user_id))

def find_by_username(username):
    return storage.find_by_username(username)

def find_record_by_id(user_id):
    return storage.find_record_by_id(user_id)

def update_profile(user_id, username, bio, filename=None):
    u = db.session.get(User, int(user_id))
    if u:
        u.username = username
        u.bio = bio
        if filename: 
            u.profile_pic = filename
        db.session.commit()

def toggle_follow(target_id):
    from flask_login import current_user
    me_id = int(current_user.id)
    if target_id == me_id: 
        return {"status": "error", "message": "Tidak bisa follow diri sendiri."}
    
    existing = Follow.query.filter_by(follower_id=me_id, followed_id=target_id).first()
    if existing:
        db.session.delete(existing)
        is_follow = False
    else:
        db.session.add(Follow(follower_id=me_id, followed_id=target_id))
        is_follow = True
    db.session.commit()
    
    follower_count = Follow.query.filter_by(followed_id=target_id).count()
    return {"status": "ok", "is_follow": is_follow, "follower_count": follower_count}

def list_other_users(me_id):
    users = User.query.filter(User.id != me_id).all()
    result = []
    for u in users:
        followers = Follow.query.filter_by(followed_id=u.id).count()
        sudah = Follow.query.filter_by(follower_id=me_id, followed_id=u.id).first() is not None
        result.append({
            "id": u.id, 
            "username": u.username, 
            "bio": u.bio, 
            "profile_pic": u.profile_pic, 
            "follower_count": followers, 
            "sudah_follow": sudah
        })
    return result

def register(username, password):
    hashed = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None