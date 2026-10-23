# 🍳 Saji - Platform Sosial Resep Masakan

Saji adalah aplikasi web berbasis komunitas di mana pengguna dapat berbagi, mencari, dan menyimpan resep masakan. Dibangun dengan fokus pada antarmuka yang modern, interaksi tanpa *reload* (AJAX), dan performa yang cepat.

## ✨ Fitur Utama

- **Autentikasi Pengguna**: Sistem login dan registrasi yang aman (Password Hashing).
- **Manajemen Profil**: Kustomisasi profil dengan fitur *upload* dan *crop* foto profil interaktif (menggunakan Cropper.js).
- **Feed & Explore**: Dapatkan rekomendasi resep dari orang yang kamu ikuti, atau jelajahi semua resep.
- **Interaksi Sosial**: Fitur mengikuti (Follow), menyukai (Like), memberi rating, dan menyimpan resep (Favorit).
- **Sistem Komentar**: Berkomentar dan membalas komentar secara *real-time* tanpa *reload* halaman.
- **Dark Mode**: Dukungan tema gelap/terang yang tersimpan di preferensi pengguna.
- **Pencarian & Filter**: Cari resep berdasarkan nama, bahan, atau kategori.

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite (dengan Flask-SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3 (Custom Design System), Vanilla JavaScript (Fetch API/AJAX)
- **Keamanan**: Flask-WTF (CSRF Protection), Werkzeug Security
- **Testing**: Pytest

## 🚀 Cara Menjalankan Secara Lokal

1. Clone repository ini:
   ```bash
   git clone https://github.com/KarsaDev314/Saji.git
   cd Saji