from core.db import db
from core.db_models import User
from services import user_service

def test_register_user(app):
    """Ngetes apakah user baru berhasil masuk ke database"""
    with app.app_context():
        # Eksekusi fungsi register
        user = user_service.register("kyo_test", "password123")
        
        # Cek apakah data beneran ada di database
        saved_user = User.query.filter_by(username="kyo_test").first()
        assert saved_user is not None
        assert saved_user.username == "kyo_test"
        assert saved_user.id == user.id

def test_find_by_username(app):
    """Ngetes apakah user bisa dicari berdasarkan username"""
    with app.app_context():
        user_service.register("sena_test", "password123")
        
        # Cari user
        found = user_service.find_by_username("sena_test")
        assert found is not None
        assert found["username"] == "sena_test"

def test_toggle_follow(app):
    """Ngetes logika follow (butuh mock current_user)"""
    # (Kita skip dulu test follow karena butuh setup request context/login)
    pass