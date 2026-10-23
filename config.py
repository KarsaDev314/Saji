import os

# Runtime
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-ganti-di-production")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
HOST = "127.0.0.1"
PORT = 5000

# Domain
KATEGORI_VALID = ("Makanan Utama", "Minuman", "Camilan", "Dessert", "Lain-lain")
RATING_VALID = (0, 1, 2, 3, 4, 5)
ADMIN_USERNAME = "admin"

# Mode tampilan
MODE_FEED = "feed"
MODE_EXPLORE = "explore"
MODE_SAYA = "saya"

# Tipe notifikasi
NOTIF_FOLLOW = "follow"
NOTIF_LIKE = "like"
NOTIF_KOMENTAR = "komentar"

# Kategori flash
FLASH_SUKSES = "sukses"
FLASH_INFO = "info"

# Batas panjang input (Ini yang tadi ilang)
MAX_NAMA = 100
MAX_WAKTU = 50
MAX_BAHAN_ITEM = 200
MAX_LANGKAH_ITEM = 500
MAX_BAHAN_COUNT = 50
MAX_LANGKAH_COUNT = 50
MAX_CATATAN = 1000
MAX_USERNAME = 30
MIN_USERNAME = 3
MIN_PASSWORD = 6
MAX_BIO = 300
MAX_KOMENTAR = 500

# Folder Upload
UPLOAD_FOLDER = "static/uploads/profiles"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}