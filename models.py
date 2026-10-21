"""Model User dan representasi publiknya."""
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password_hash, bio, join_date):
        self.id = str(id)
        self.username = username
        self.password_hash = password_hash
        self.bio = bio
        self.join_date = join_date


def to_public_dict(record):
    """Konversi record user (dict JSON) ke bentuk yang aman ditampilkan."""
    return {
        "id": record["id"],
        "username": record["username"],
        "bio": record.get("bio", ""),
        "join_date": record.get("join_date", ""),
    }