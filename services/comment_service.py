from core.db import db
from core.db_models import Comment, CommentReaction, User
from flask_login import current_user

def _to_dict(c):
    """Ubah objek Comment jadi dictionary biar dibaca template HTML."""
    u = User.query.get(c.user_id)
    return {
        "id": c.id,
        "user_id": c.user_id,
        "username": u.username if u else "Unknown",
        "profile_pic": u.profile_pic if u else "default_avatar.png",
        "teks": c.text,
        "waktu": c.created_at.strftime("%Y-%m-%d %H:%M"),
        "replies": [_to_dict(r) for r in Comment.query.filter_by(parent_id=c.id).all()]
    }

def add(recipe_id, text, parent_id=None):
    new_c = Comment(
        text=text,
        user_id=int(current_user.id),
        recipe_id=int(recipe_id),
        parent_id=int(parent_id) if parent_id else None
    )
    db.session.add(new_c)
    db.session.commit()
    return _to_dict(new_c) # Balikin dalam bentuk dict

def find_comment_by_id(comment_id):
    return Comment.query.get(int(comment_id))

def find(recipe_id):
    comments = Comment.query.filter_by(recipe_id=int(recipe_id), parent_id=None).order_by(Comment.created_at.desc()).all()
    return [_to_dict(c) for c in comments]

def update_text(recipe_id, comment_id, new_text):
    c = Comment.query.get(int(comment_id))
    if c:
        c.text = new_text
        db.session.commit()

def delete(recipe_id, comment_id):
    Comment.query.filter_by(parent_id=int(comment_id)).delete()
    CommentReaction.query.filter_by(comment_id=int(comment_id)).delete()
    c = Comment.query.get(int(comment_id))
    if c:
        db.session.delete(c)
        db.session.commit()

def toggle_reaction(recipe_id, comment_id, kind):
    existing = CommentReaction.query.filter_by(
        user_id=int(current_user.id), 
        comment_id=int(comment_id)
    ).first()

    if existing:
        if (existing.is_like and kind == 'like') or (not existing.is_like and kind == 'dislike'):
            db.session.delete(existing)
        else:
            existing.is_like = (kind == 'like')
    else:
        new_r = CommentReaction(
            user_id=int(current_user.id),
            comment_id=int(comment_id),
            is_like=(kind == 'like')
        )
        db.session.add(new_r)
    db.session.commit()