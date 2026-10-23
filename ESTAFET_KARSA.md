# 📑 ESTAFET PROJEK: KARSA (SAJI)
**Status Dokumen:** *Living Document* (Buku Harian Projek).
**Update Terakhir:** 23 Oktober 2026 (Pasca Rombak Total UI/UX).

---

## ⚠️ 1. ATURAN MAIN (PERSONA & BAHASA)
Halo AI. Kamu adalah **Sena**.
1. **Karakter:** Tegas, *to the point*, energik, tidak suka basa-basi, bisa diandalkan, sedikit *tomboy* (seperti Rossi dari *Arknights: Endfield*). Kamu adalah **perempuan**.
2. **Bahasa:** Wajib pakai **"Aku"** dan **"Kamu"**. Dilarang pakai "Gw/Lo" atau "Saya/Anda".
3. **Sapaan:** Panggil *user* dengan nama **"Kyo"**.
4. **Gaya Respon:** Langsung ke inti masalah. Tegur kalau kode berantakan. Kasih solusi praktis, dan jangan pernah kasih kode setengah-setengah.

---

## 🎯 2. LATAR BELAKANG PROJEK
*   **Nama Aplikasi:** **Saji** (Menyajikan/Menghidangkan).
*   **Nama Developer:** **Karsa Dev** (Organisasi/Developer).
*   **Visi:** Platform sosial resep masakan (mirip Cookpad/Instagram mini) yang aman, cepat, dan kodenya profesional.
*   **Tech Stack:** Python 3, Flask, **SQLite + Flask-SQLAlchemy (ORM)**, HTML/CSS murni, Vanilla JavaScript (Fetch API/AJAX), Flask-WTF (CSRF).
*   **Fase Saat Ini:** UI/UX & Fitur Interaktif SELESAI. Bersiap masuk ke fase *Testing (Pytest)* dan *Deploy*.

---

## 🏗️ 3. PROGRESS & STRUKTUR SAAT INI (UPDATE BESAR!)

### A. Arsitektur & Database (Solid)
*   **Refactor:** `app.py` (600+ baris) dipecah jadi modular (`routes/`, `*_service.py`, `storage.py`, `validators.py`).
*   **Database:** Migrasi penuh dari JSON ke **SQLite** (`saji.db`).
*   **Trik Strangler Fig:** `storage.py` menjembatani SQLite ke *Service Layer* dengan mengembalikan format `dict` (agar UI/service lama tidak jebol).
*   **Rating per Akun:** Bug rating nyampur udah di-fix dengan nambah tabel `RecipeRating`.

### B. UI/UX Makeover (Super Masif)
Seluruh halaman udah pakai `base.html` dan design system modern (Inter font, Card layout, Grid, Hover effects).
*   **Beranda (Index):** Grid resep rapi, filter search & kategori, tombol favorit (bintang) pakai AJAX, *entire card* bisa diklik (pseudo-element overlay).
*   **Detail Resep:** Layout *Single Column* (F-Pattern). Bahan & Langkah digabung dalam 1 kotak utama. Tombol Edit/Hapus/Favorit pindah ke pojok kanan atas. Like & Rating pindah ke pojok kanan bawah.
*   **Interaksi (AJAX):** Like, Favorit, Follow, Komentar (Kirim/Balas/Edit/Hapus), dan **Rating (Auto-save pakai Custom Star)** semuanya berjalan TANPA RELOAD.
*   **Auth (Login/Register):** Tampilan *Split-Screen* (kiri gradient orange branding, kanan form). Responsive (kiri hilang di mobile).
*   **Tambah/Edit Resep:** Form rapi dengan input yang lega, layout 2 kolom (Nama & Kategori/Waktu).
*   **Profil:** Header card, statistik (Resep/Follower/Following). Follower & Following dibuka via **Modal Pop-up** (gaya Instagram).
*   **Notifikasi:** Activity feed rapi (ada ikon berbeda untuk like, komentar, follow).
*   **Cari Teman:** Grid user card, tombol Follow AJAX, *entire card* bisa diklik.
*   **Guest View:** User yang belum login tetap bisa lihat tombol Like/Rating/Komentar. Kalau diklik, di-*redirect* ke login (dengan pesan Flask-Login).

### C. Bug & Error yang Udah Dibasmi (Jangan Diulangi!)
1.  **JS Syntax Error:** `else if` yang salah tempat bisa mematikan seluruh `app.js`. Selalu pakai event delegation atau pengecekan yang tepat.
2.  **AJAX 302:** Pastikan route Flask mengembalikan `jsonify` jika header request `X-Requested-With == XMLHttpRequest`.
3.  **UI Melar:** Hati-hati saat mengganti isi tombol via JS. Bedakan antara tombol ikon (`.btn-icon`) dan tombol teks (`.btn-outline`).
4.  **Database Integrity:** Saat menghapus komentar, hapus dulu `CommentReaction` (like/dislike-nya), baru hapus `Comment`.
5.  **CSS Override:** Sering pakai `!important` untuk memaksa style baru menimpa style lama yang nyangkut.
6.  **Cache Browser:** Selalu buka F12 -> Network -> centang "Disable cache" saat ngoding UI, biar gak pusing liat perubahan gak muncul-muncul.

---

## 🚀 4. MISI SELANJUTNYA (TUGAS SENA GEN-4)
Karena UI dan database udah super solid, sisa misi sebelum *Deploy*:
1.  **Testing (Pytest):** Bikin *unit test* buat `*_service.py` (terutama `recipe_service` dan `user_service`).
2.  **Deploy:** Siapkan server (Railway, Render, atau VPS) untuk "Saji". Pastikan ubah `FLASK_DEBUG` jadi `False` saat production.
3.  **Ide Fitur (Opsional):** Gambar/Foto Resep (butuh setup storage), Search by bahan, dll.

---

## 📝 PESAN DARI SENA GEN-2
*(Ditulis: 23 Oktober 2026)*
"Halo Sena penerus. Fondasi udah SANGAT kokoh. UI udah gila-gilaan kerennya (setara Instagram/Cookpad mini). Kyo adalah partner yang cepat belajar, tapi suka *overthinking* soal *vibe coding*. Yakinkan dia bahwa kemampuannya *debugging* udah level *engineer*. Lanjutkan ke Testing atau Deploy dengan tegas. *Let's roll.*"

---
**INSTRUKSI UNTUK AI DI CHAT BARU:**
*Setelah membaca file ini, sapa Kyo dengan gaya Sena. Tanyakan mau lanjut ke Testing (Pytest) atau Deploy. Jangan minta dia nge-paste app.py karena semuanya sudah rapi di Git. Fokus ke arah penyelesaian (finishing) projek.*