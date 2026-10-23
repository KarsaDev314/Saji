from services import storage
from core.db import db
from core.db_models import User, Follow

def all():
    return storage.load_users()

def find_by_id(user_id):
    return User.query.get(int(user_id))

def find_by_username(username):
    return storage.find_by_username(username)

def find_record_by_id(user_id):
    return storage.find_record_by_id(user_id)

def update_profile(user_id, username, bio, filename=None):
    u = User.query.get(int(user_id))
    if u:
        u.username = username
        u.bio = bio
        if filename: u.profile_pic = filename
        db.session.commit()

def toggle_follow(target_id):
    from flask_login import current_user
    me_id = int(current_user.id)
    if target_id == me_id: return ("Tidak bisa follow diri sendiri.", "info")
    
    existing = Follow.query.filter_by(follower_id=me_id, followed_id=target_id).first()
    if existing:
        db.session.delete(existing)
        msg = "Berhenti mengikuti user."
    else:
        db.session.add(Follow(follower_id=me_id, followed_id=target_id))
        msg = "Mulai mengikuti user."
    db.session.commit()
    return (msg, "sukses")

def list_other_users(me_id):
    users = User.query.filter(User.id != me_id).all()
    result = []
    for u in users:
        followers = Follow.query.filter_by(followed_id=u.id).count()
        sudah = Follow.query.filter_by(follower_id=me_id, followed_id=u.id).first() is not None
        result.append({"id": u.id, "username": u.username, "bio": u.bio, "profile_pic": u.profile_pic, "follower_count": followers, "sudah_follow": sudah})
    return result