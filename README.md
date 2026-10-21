# 🍳 Panduan Memasak

Aplikasi web sederhana untuk menyimpan, mencari, dan melihat resep masakan.
Dibuat dengan Python + Flask, data disimpan di file JSON.

---

## ✨ Fitur

- 📋 Lihat daftar semua resep
- 🔍 Cari resep berdasarkan **nama** atau **bahan**
- 📖 Lihat detail resep (bahan + langkah memasak)
- ➕ Tambah resep baru
- ✏️ Edit resep yang sudah ada
- 🗑 Hapus resep (dengan konfirmasi)

---

## 🛠️ Teknologi

- **Python 3** — bahasa pemrograman
- **Flask** — framework web (ringan, cocok untuk pemula)
- **JSON** — format penyimpanan data (`resep.json`)
- **HTML + CSS** — tampilan halaman

Tidak ada database. Tidak butuh server online. Semua jalan di komputer sendiri.

---

## 📦 Prasyarat

1. **Python 3.8+** terinstall. Cek dengan:
   ```
   python --version
   ```
2. **Flask** terinstall. Kalau belum:
   ```
   pip install flask
   ```

---

## 🚀 Cara Menjalankan

1. Buka terminal di folder ini.
2. Jalankan:
   ```
   python app.py
   ```
3. Akan muncul pesan:
   ```
   Running on http://127.0.0.1:5000
   ```
4. Buka browser, akses: **http://127.0.0.1:5000**
5. Untuk menghentikan server: tekan **Ctrl + C** di terminal.

---

## 📁 Struktur Folder

```
panduan_masak/
├── app.py                  ← kode utama Flask (route & logika)
├── resep.json              ← data semua resep
├── resep_backup.json       ← cadangan data (opsional)
├── README.md               ← file ini
├── templates/              ← file HTML
│   ├── index.html          ← halaman daftar + pencarian
│   ├── detail.html         ← halaman detail resep
│   └── tambah.html         ← form tambah/edit resep
└── static/                 ← file non-HTML
    └── style.css           ← tampilan (warna, layout)
```

---

## 🗂️ Format Data (resep.json)

```json
{
  "resep": [
    {
      "id": 1,
      "nama": "Nasi Goreng",
      "kategori": "Makanan Utama",
      "waktu": "20 menit",
      "bahan": ["2 piring nasi", "2 butir telur"],
      "langkah": ["Panaskan minyak.", "Tumis bawang."]
    }
  ]
}
```

- `id` — angka unik, dibuat otomatis saat tambah resep
- `bahan` & `langkah` — array (daftar) string, satu item per baris saat input

---

## 💡 Tips

- **Backup data:** sebelum eksperimen besar, copy `resep.json` jadi `resep_backup.json`.
- **Reset data:** kalau mau mulai dari kosong, timpa `resep.json` dengan:
  ```json
  { "resep": [] }
  ```
- **Ganti warna tema:** buka `static/style.css`, cari `#d35400` (oranye), ganti dengan warna lain. Contoh: `#2980b9` (biru), `#27ae60` (hijau).

---

## 📝 Catatan Pengembangan

Dibuat sebagai proyek belajar Flask, dengan milestone:
1. ✅ Web app + daftar resep
2. ✅ Halaman detail
3. ✅ Pencarian
4. ✅ Form tambah resep
5. ✅ Hapus resep
6. ✅ Edit resep

**Status:** CRUD lengkap, siap dikembangkan lebih lanjut.