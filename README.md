# 🍳 Saji - Panduan Memasak

Platform sosial berbagi resep masakan. Dibangun dengan fokus pada kebersihan kode (Clean Code), keamanan, dan pengalaman pengguna yang interaktif.

Dikembangkan oleh **Karsa Dev**.

---

## 🚀 Fitur Utama
- **Autentikasi**: Register, Login, Logout (Flask-Login).
- **CRUD Resep**: Tambah, Edit, Hapus, dan Lihat Detail Resep.
- **Sosial**: Follow/Unfollow pengguna, Feed, Explore, dan Profil.
- **Interaksi (AJAX)**: Like, Favorit, Komentar (bersarang), dan Follow tanpa perlu me-reload halaman.
- **Notifikasi**: Pemberitahuan otomatis saat ada interaksi.
- **Keamanan**: CSRF Protection (Flask-WTF), Password Hashing, dan Session Hardening.

## 🛠️ Tech Stack
- **Backend**: Python 3, Flask
- **Database**: SQLite + Flask-SQLAlchemy (ORM)
- **Frontend**: HTML5, Modern CSS (Grid/Flexbox), Vanilla JavaScript (Fetch API)
- **Arsitektur**: Modular (Routes, Services, Models)

## ⚙️ Cara Menjalankan (Lokal)

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/KarsaDev314/Saji.git
   cd Saji