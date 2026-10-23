import pytest
from app import create_app
from core.db import db

@pytest.fixture
def app():
    # Pake database in-memory biar cepet dan gak ngotori saji.db asli
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False # Matiin CSRF pas testing
    })

    with app.app_context():
        db.create_all() # Bikin tabel kosong
        yield app
        db.session.remove()
        db.drop_all() # Hapus semua pas test selesai

@pytest.fixture
def client(app):
    return app.test_client()