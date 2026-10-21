"""Satu-satunya pintu baca/tulis JSON. Tidak ada modul lain yang buka file."""
import json

import config
from extensions import db_lock


def _load(path, key):
    with db_lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)[key]
        except (FileNotFoundError, json.JSONDecodeError):
            return []


def _save(path, key, data):
    with db_lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({key: data}, f, ensure_ascii=False, indent=2)


def load_users():
    return _load(config.USERS_FILE, "users")


def save_users(users):
    _save(config.USERS_FILE, "users", users)


def load_recipes():
    return _load(config.DATA_FILE, "resep")


def save_recipes(recipes):
    _save(config.DATA_FILE, "resep", recipes)


def load_notifications():
    return _load(config.NOTIF_FILE, "notifikasi")


def save_notifications(items):
    _save(config.NOTIF_FILE, "notifikasi", items)