"""Operasi bisnis user."""
from datetime import datetime

from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash

import config
import notification_service
import storage
from models import User


def all():
    return storage.load_users()


def find_by_id(user_id):
    for u in storage.load_users():
        if u["id"] == int(user_id):
            return User(u["id"], u["username"], u["password_hash"],
                        u.get("bio", ""), u.get("join_date", ""))
    return None


def find_record_by_id(user_id):
    for u in storage.load_users():
        if u["id"] == int(user_id):
            return u
    return None


def find_by_username(username):
    for u in storage.load_users():
        if u["username"].lower() == username.lower():
            return u
    return None


def current_record():
    """Record user yang login, atau None."""
    if not current_user.is_authenticated:
        return None
    return find_record_by_id(int(current_user.id))


def register(username, password):
    users = storage.load_users()
    new_id = max((u["id"] for u in users), default=0) + 1
    record = {
        "id": new_id,
        "username": username,
        "password_hash": generate_password_hash(password),
        "bio": "",
        "join_date": datetime.now().strftime("%Y-%m-%d"),
        "following": [],
        "favorit_ids": [],
    }
    users.append(record)
    storage.save_users(users)
    return User(new_id, username, record["password_hash"], "", record["join_date"])


def authenticate(username, password):
    record = find_by_username(username)
    if not record or not check_password_hash(record["password_hash"], password):
        return None
    return User(record["id"], record["username"], record["password_hash"],
                record.get("bio", ""), record.get("join_date", ""))


def update_profile(user_id, username, bio):
    users = storage.load_users()
    for u in users:
        if u["id"] == int(user_id):
            u["username"] = username
            u["bio"] = bio
            break
    storage.save_users(users)


def follow_stats(users, user_id):
    """Return (follower_count, following_count, following_users, followers_list)."""
    following_ids = next(
        (u.get("following", []) for u in users if u["id"] == user_id), []
    )
    following_users = [u for u in users if u["id"] in following_ids]
    
    # Cari siapa aja yang nge-follow user ini
    followers_list = [u for u in users if user_id in u.get("following", [])]
    
    return len(followers_list), len(following_ids), following_users, followers_list


def toggle_follow(target_id):
    """Return (pesan, kategori) atau None kalau target tidak ada."""
    me_id = int(current_user.id)
    if target_id == me_id:
        return ("Tidak bisa follow diri sendiri.", config.FLASH_INFO)

    users = storage.load_users()
    if not any(u["id"] == target_id for u in users):
        return None

    pesan, kategori = "Mulai mengikuti user.", config.FLASH_SUKSES
    for u in users:
        if u["id"] == me_id:
            following = u.setdefault("following", [])
            if target_id in following:
                following.remove(target_id)
                pesan, kategori = "Berhenti mengikuti user.", config.FLASH_INFO
            else:
                following.append(target_id)
                notification_service.send(
                    target_id, me_id, config.NOTIF_FOLLOW,
                    "mulai mengikuti kamu",
                    f"/profil/{current_user.username}",
                )
            break
    storage.save_users(users)
    return (pesan, kategori)


def list_other_users(me_id):
    users = storage.load_users()
    me = next((u for u in users if u["id"] == me_id), None)
    following = me.get("following", []) if me else []

    result = []
    for u in users:
        if u["id"] == me_id:
            continue
        follower_count = sum(1 for x in users if u["id"] in x.get("following", []))
        result.append({
            "id": u["id"],
            "username": u["username"],
            "bio": u.get("bio", ""),
            "follower_count": follower_count,
            "sudah_follow": u["id"] in following,
        })
    return result