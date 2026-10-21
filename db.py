"""Instance SQLAlchemy. Di-init di app.py, dipakai di semua service."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()