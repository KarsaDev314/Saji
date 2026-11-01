"""
Script sekali-pakai: hapus foto profil yang user-nya udah nggak ada
atau foto lama yang nggak dipakai di DB.
Jalankan: python cleanup_orphan_photos.py
"""
import os
import sqlite3

DB_PATH = "saji.db"
UPLOAD_DIR = os.path.join("static", "uploads", "profiles")


def main():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, username, profile_pic FROM users").fetchall()
    conn.close()

    valid_files = {r[2] for r in rows if r[2] and r[2] != "default_avatar.png"}
    valid_users = {r[0] for r in rows}

    print(f"User di DB       : {len(valid_users)} -> {sorted(valid_users)}")
    print(f"File valid di DB : {len(valid_files)} -> {sorted(valid_files)}")
    print()

    if not os.path.isdir(UPLOAD_DIR):
        print(f"[SKIP] Folder {UPLOAD_DIR} nggak ada.")
        return

    orphans = []
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        if fname in valid_files:
            continue
        try:
            uid = int(fname.split("_")[1])
        except (IndexError, ValueError):
            print(f"[SKIP] Format aneh: {fname}")
            continue
        if uid not in valid_users:
            orphans.append((fname, "user sudah dihapus"))
        else:
            orphans.append((fname, "foto lama, sudah diganti"))

    if not orphans:
        print("[OK] Nggak ada orphan. Bersih!")
        return

    print(f"[FOUND] {len(orphans)} file orphan:\n")
    for fname, reason in orphans:
        print(f"  - {fname:25s} ({reason})")

    confirm = input("\nHapus semua? Ketik 'HAPUS': ").strip()
    if confirm != "HAPUS":
        print("Batal. Nggak ada yang dihapus.")
        return

    for fname, _ in orphans:
        fpath = os.path.join(UPLOAD_DIR, fname)
        try:
            os.remove(fpath)
            print(f"  [X] Dihapus: {fname}")
        except OSError as e:
            print(f"  [!] Gagal hapus {fname}: {e}")

    print(f"\n[DONE] {len(orphans)} file diproses.")


if __name__ == "__main__":
    main()