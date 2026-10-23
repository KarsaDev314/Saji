from core.db import db
from core.db_models import Notification
from flask_login import current_user

def unread_count(user_id):
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()

def fetch_and_mark_read(user_id):
    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    for n in notifs:
        n.is_read = True
    db.session.commit()
    return [{"id": n.id, "message": n.message, "created_at": n.created_at} for n in notifs]