"""
Tambah kolom yang hilang di tabel recipes tanpa hapus DB.
Aman dijalankan berkali-kali (idempotent).
"""
from app import create_app
from core.db import db
from sqlalchemy import text


def migrate():
    app = create_app()
    with app.app_context():
        # Kasih tau DB-nya di mana
        print(f"[i] DB URL: {db.engine.url}")

        with db.engine.connect() as conn:
            # Cek kolom existing di tabel recipes
            result = conn.execute(text("PRAGMA table_info(recipes)"))
            cols = [row[1] for row in result]
            print(f"[i] Kolom saat ini di 'recipes': {cols}")

            changed = []

            if "rating" not in cols:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN rating INTEGER DEFAULT 0"
                ))
                changed.append("rating")

            if "catatan" not in cols:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN catatan VARCHAR(255) DEFAULT ''"
                ))
                changed.append("catatan")

            conn.commit()

        if changed:
            print(f"[✓] Kolom ditambahkan: {changed}")
        else:
            print("[✓] Semua kolom udah ada, nggak ada yang perlu diubah.")

        # Verifikasi akhir
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(recipes)"))
            cols = [row[1] for row in result]
            print(f"[i] Kolom final di 'recipes': {cols}")


if __name__ == "__main__":
    migrate()