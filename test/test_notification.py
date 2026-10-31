"""
Test untuk route & logic Notifikasi.
Route: GET /notifications (auto mark-as-read saat dibuka)
"""
from core.db import db
from core.db_models import Notification, User


def _register_and_login(client, username="notifuser", password="password123"):
    """Helper: pastikan session bersih, register, lalu login."""
    # Paksa hapus session cookie biar nggak bocor dari test lain
    with client.session_transaction() as sess:
        sess.clear()

    client.post('/register', data={
        'username': username,
        'password': password,
        'password2': password,
    }, follow_redirects=True)
    client.post('/login', data={
        'username': username,
        'password': password,
    }, follow_redirects=True)


def test_notifications_redirects_without_login(client):
    """Belum login -> harus redirect ke /login"""
    # Pastikan bener-bener bersih
    with client.session_transaction() as sess:
        sess.clear()

    response = client.get('/notifications')
    assert response.status_code == 302
    assert '/login' in response.location


def test_notifications_accessible_when_logged_in(client):
    """Login -> halaman notifikasi ke-load 200"""
    _register_and_login(client, username="notifuser_a")
    response = client.get('/notifications', follow_redirects=True)
    assert response.status_code == 200


def test_notifications_marked_as_read_on_visit(client, app):
    """Setiap buka /notifications, semua notif user otomatis is_read=True"""
    _register_and_login(client, username="notif_read")

    with app.app_context():
        user = User.query.filter_by(username="notif_read").first()
        assert user is not None, "User gagal terbuat di DB"
        
        db.session.add(Notification(user_id=user.id, message="Notif 1"))
        db.session.add(Notification(user_id=user.id, message="Notif 2"))
        db.session.commit()

        unread_before = Notification.query.filter_by(user_id=user.id, is_read=False).count()
        assert unread_before == 2

    # Buka halaman notifikasi
    response = client.get('/notifications', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="notif_read").first()
        unread_after = Notification.query.filter_by(user_id=user.id, is_read=False).count()
        assert unread_after == 0
        total = Notification.query.filter_by(user_id=user.id).count()
        assert total == 2


def test_notification_isolated_per_user(client, app):
    """Notif user A tidak ke-mark-read saat user B buka /notifications"""
    # Setup user A & notifnya
    _register_and_login(client, username="user_a")
    with app.app_context():
        user_a = User.query.filter_by(username="user_a").first()
        db.session.add(Notification(user_id=user_a.id, message="Pesan untuk A"))
        db.session.commit()
        user_a_id = user_a.id

    # Logout (WAJIB pakai POST, bukan GET)
    client.post('/logout', follow_redirects=True)

    # Setup user B & buka notif
    _register_and_login(client, username="user_b")
    client.get('/notifications', follow_redirects=True)

    # Cek notif user A harus tetap unread
    with app.app_context():
        unread_a = Notification.query.filter_by(user_id=user_a_id, is_read=False).count()
        assert unread_a == 1, "Notif user A ikut ke-mark-read, ada bug isolasi!"