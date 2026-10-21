"""Operasi bisnis komentar."""
from datetime import datetime
import uuid

from flask_login import current_user

import config
import notification_service
import storage


def find(comments, comment_id):
    """Cari komentar by ID, rekursif ke balasan."""
    for c in comments:
        if c.get("id") == comment_id:
            return c
        if c.get("replies"):
            found = find(c["replies"], comment_id)
            if found:
                return found
    return None


def add(recipe_id, text, parent_id=None):
    """Tambah komentar. Return True kalau berhasil, False kalau gagal."""
    recipes = storage.load_recipes()
    uid = int(current_user.id)

    target = None
    for r in recipes:
        if r["id"] == recipe_id:
            target = r
            break
    if target is None:
        return False

    new_comment = {
        "id": str(uuid.uuid4())[:8],
        "user_id": uid,
        "username": current_user.username,
        "teks": text[:config.MAX_KOMENTAR],
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "likes": [], "dislikes": [], "replies": [],
    }

    added = False
    if parent_id:
        parent = find(target.get("comments", []), parent_id)
        if parent:
            parent["replies"].append(new_comment)
            added = True
    else:
        target.setdefault("comments", []).append(new_comment)
        added = True

    storage.save_recipes(recipes)

    if added and target.get("user_id", 0) not in (0, uid):
        notification_service.send(
            target["user_id"], uid, config.NOTIF_KOMENTAR,
            f"mengomentari resepmu '{target['nama']}'",
            f"/resep/{recipe_id}",
        )
    return added


def update_text(recipe_id, comment_id, new_text):
    recipes = storage.load_recipes()
    for r in recipes:
        if r["id"] != recipe_id:
            continue
        c = find(r.get("comments", []), comment_id)
        if c:
            c["teks"] = new_text[:config.MAX_KOMENTAR]
        break
    storage.save_recipes(recipes)


def delete(recipe_id, comment_id):
    recipes = storage.load_recipes()
    for r in recipes:
        if r["id"] != recipe_id:
            continue
        r["comments"] = _remove_recursive(r.get("comments", []), comment_id)
        break
    storage.save_recipes(recipes)


def _remove_recursive(comments, target_id):
    result = []
    for c in comments:
        if c.get("id") == target_id:
            continue
        if c.get("replies"):
            c["replies"] = _remove_recursive(c["replies"], target_id)
        result.append(c)
    return result


def toggle_reaction(recipe_id, comment_id, kind):
    """kind: 'like' atau 'dislike'. Like/dislike saling eksklusif."""
    same, opposite = ("likes", "dislikes") if kind == "like" else ("dislikes", "likes")
    recipes = storage.load_recipes()
    uid = int(current_user.id)

    for r in recipes:
        if r["id"] != recipe_id:
            continue
        c = find(r.get("comments", []), comment_id)
        if not c:
            break
        if uid in c.get(opposite, []):
            c[opposite].remove(uid)
        if uid in c.get(same, []):
            c[same].remove(uid)
        else:
            c[same].append(uid)
        break
    storage.save_recipes(recipes)