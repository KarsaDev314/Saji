"""
Test untuk route Bug Report.
- POST /api/bugs (bisa anonim & login, pakai form field "pesan_bug")
- GET  /admin/bugs (admin only, cek username == config.ADMIN_USERNAME)
- POST /admin/bugs/<id>/resolve (admin only, ubah status -> resolved)
"""
import config
from core.db import db
from core.db_models import BugReport, User


def _register_and_login(client, username, password="password123"):
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


# ---------- /api/bugs ----------

def test_submit_bug_anonymous_success(client, app):
    """Anonim bisa lapor bug, user_id tetap None di DB"""
    with client.session_transaction() as sess:
        sess.clear()
        
    response = client.post('/api/bugs', data={'pesan_bug': 'Ada bug di halaman profil'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

    with app.app_context():
        report = BugReport.query.filter_by(message='Ada bug di halaman profil').first()
        assert report is not None
        assert report.user_id is None
        assert report.status == 'pending'


def test_submit_bug_empty_message_returns_400(client):
    """Pesan kosong -> 400 + status error"""
    response = client.post('/api/bugs', data={'pesan_bug': '   '})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_submit_bug_logged_in_attaches_user_id(client, app):
    """Login -> bug tersimpan dengan user_id bener"""
    _register_and_login(client, username="bugreporter")

    response = client.post('/api/bugs', data={'pesan_bug': 'Bug dari user login'})
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="bugreporter").first()
        report = BugReport.query.filter_by(message='Bug dari user login').first()
        assert report is not None
        assert report.user_id == user.id


# ---------- /admin/bugs ----------

def test_admin_page_redirects_without_login(client):
    """Anonim akses /admin/bugs -> redirect ke login"""
    with client.session_transaction() as sess:
        sess.clear()
        
    response = client.get('/admin/bugs')
    assert response.status_code == 302
    assert '/login' in response.location


def test_admin_page_forbidden_for_normal_user(client):
    """User biasa (bukan admin) -> 403"""
    _register_and_login(client, username="bukanadmin")
    response = client.get('/admin/bugs')
    assert response.status_code == 403


def test_admin_page_accessible_for_admin(client, app):
    """User dengan username == config.ADMIN_USERNAME -> 200"""
    _register_and_login(client, username=config.ADMIN_USERNAME)
    response = client.get('/admin/bugs')
    assert response.status_code == 200


def test_resolve_bug_changes_status(client, app):
    """Admin resolve bug -> status jadi 'resolved'"""
    # 1. Bikin bug via anonim
    client.post('/api/bugs', data={'pesan_bug': 'Bug yang mau di-resolve'})

    with app.app_context():
        report = BugReport.query.filter_by(message='Bug yang mau di-resolve').first()
        assert report is not None
        bug_id = report.id
        assert report.status == 'pending'

    # 2. Login sebagai admin
    _register_and_login(client, username=config.ADMIN_USERNAME)

    # 3. Resolve
    response = client.post(f'/admin/bugs/{bug_id}/resolve', follow_redirects=True)
    assert response.status_code == 200

    # 4. Cek status
    with app.app_context():
        report = db.session.get(BugReport, bug_id)
        assert report.status == 'resolved'