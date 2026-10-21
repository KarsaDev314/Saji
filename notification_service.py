"""Operasi notifikasi."""
from datetime import datetime
import uuid

from flask_login import current_user

import config
import storage


def send(recipient_id, sender_id, type_, message, link):
    """Kirim notif kalau penerima bukan pengirim."""
    if int(recipient_id) == int(sender_id):
        return

    items = storage.load_notifications()
    items.append({
        "id": str(uuid.uuid4())[:8],
        "penerima_id": int(recipient_id),
        "pengirim_id": int(sender_id),
        "pengirim_username": current_user.username,
        "tipe": type_,
        "pesan": message,
        "tautan": link,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "dibaca": False,
    })
    storage.save_notifications(items)


def fetch_and_mark_read(user_id):
    """Ambil notif user, urut terbaru, sekaligus tandai sudah dibaca."""
    uid = int(user_id)
    items = storage.load_notifications()
    mine = [n for n in items if n["penerima_id"] == uid]

    changed = False
    for n in items:
        if n["penerima_id"] == uid and not n["dibaca"]:
            n["dibaca"] = True
            changed = True
    if changed:
        storage.save_notifications(items)

    mine.sort(key=lambda n: n["waktu"], reverse=True)
    return mine


def unread_count(user_id):
    uid = int(user_id)
    return sum(
        1 for n in storage.load_notifications()
        if n["penerima_id"] == uid and not n["dibaca"]
    )