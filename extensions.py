"""Ekstensi Flask dan lock global untuk semua file data."""
from threading import RLock
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
login_manager = LoginManager()
db_lock = RLock()