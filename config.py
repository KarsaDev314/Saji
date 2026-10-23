import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
HOST = "127.0.0.1"
PORT = 5000
KATEGORI_VALID = ("Makanan Utama", "Minuman", "Camilan", "Dessert", "Lain-lain")
MODE_FEED = "feed"
MODE_EXPLORE = "explore"
MODE_SAYA = "saya"
FLASH_SUKSES = "sukses"
FLASH_INFO = "info"
UPLOAD_FOLDER = "static/uploads/profiles"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}