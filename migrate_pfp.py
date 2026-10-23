import sqlite3
conn = sqlite3.connect('saji.db')
try:
    conn.execute("ALTER TABLE users ADD COLUMN profile_pic VARCHAR(200) DEFAULT 'default_avatar.png' NOT NULL")
    conn.commit()
    print("Migrasi sukses!")
except Exception as e:
    print("Error (mungkin kolom sudah ada):", e)
finally:
    conn.close()