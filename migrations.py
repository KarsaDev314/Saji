"""Migrasi skema data lama ke skema baru. Idempoten, aman dijalankan berulang."""
import uuid

import storage


def migrate_users():
    """Pastikan setiap user punya field 'following' dan 'favorit_ids'."""
    users = storage.load_users()
    changed = False
    for u in users:
        for key in ("following", "favorit_ids"):
            if key not in u:
                u[key] = []
                changed = True
    if changed:
        storage.save_users(users)


def migrate_recipes():
    """Pastikan setiap resep punya field baru + komentar punya ID/likes/replies."""
    recipes = storage.load_recipes()
    changed = False
    for r in recipes:
        for key, default in (
            ("favorit", False), ("rating", 0), ("catatan", ""),
            ("user_id", 0), ("likes", []), ("comments", []),
        ):
            if key not in r:
                r[key] = default
                changed = True
        for c in r.get("comments", []):
            if "id" not in c:
                c["id"] = str(uuid.uuid4())[:8]
                changed = True
            for key in ("likes", "dislikes", "replies"):
                if key not in c:
                    c[key] = []
                    changed = True
    if changed:
        storage.save_recipes(recipes)


def run_all():
    """Jalankan semua migrasi. Dipanggil sekali saat app start."""
    migrate_users()
    migrate_recipes()