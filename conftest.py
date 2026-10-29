import pytest
from app import create_app
from core.db import db as _db

@pytest.fixture(scope='session')
def app():
    # Bikin app pakai konfigurasi testing
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', # Pakai RAM, bukan file saji.db
        'WTF_CSRF_ENABLED': False, # Matiin CSRF biar gampang ngetes form
        'SERVER_NAME': 'localhost.localdomain'
    })

    with app.app_context():
        _db.create_all() # Bikin tabel
        yield app        # Jalanin tes
        _db.drop_all()   # Hapus tabel setelah selesai

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()