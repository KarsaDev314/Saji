"""
Seed data resep buat Saji.
Jalankan SEKALI: python seed_recipes.py
Aman dijalankan berkali-kali (idempotent) — nggak bakal dobel.
"""
from app import create_app
from core.db import db
from core.db_models import User, Recipe


RECIPES = [
    {
        "nama": "Nasi Goreng Kampung",
        "kategori": "Makanan Utama",
        "waktu": "20 menit",
        "bahan": "2 piring nasi putih\n2 siung bawang merah\n1 siung bawang putih\n2 buah cabai rawit\n1 butir telur\n2 sdm kecap manis\nGaram secukupnya\nMinyak goreng",
        "langkah": "1. Haluskan bawang merah, bawang putih, cabai.\n2. Tumis bumbu halus sampai harum.\n3. Masukkan telur, orak-arik.\n4. Masukkan nasi, aduk rata.\n5. Tambahkan kecap dan garam, aduk hingga matang.\n6. Sajikan hangat.",
        "rating": 5,
        "catatan": "Pakai nasi sisa semalam biar nggak lembek.",
    },
    {
        "nama": "Sate Ayam Madura",
        "kategori": "Makanan Utama",
        "waktu": "45 menit",
        "bahan": "500g daging ayam fillet\nTusuk sate secukupnya\n3 sdm kecap manis\n2 sdm kacang tanah goreng halus\n2 siung bawang putih\n3 siung bawang merah\n1 sdt ketumbar\nGaram dan gula jawa",
        "langkah": "1. Potong ayam kotak-kotak.\n2. Rendam dengan kecap, bawang, ketumbar 15 menit.\n3. Tusuk ayam di tusuk sate.\n4. Bakar sambil diolesi sisa bumbu.\n5. Bumbu kacang: haluskan kacang, bawang, kecap, garam.\n6. Sajikan sate dengan bumbu kacang dan irisan bawang.",
        "rating": 5,
        "catatan": "Rendam tusuk sate dulu biar nggak gosong.",
    },
    {
        "nama": "Rendang Daging Sapi",
        "kategori": "Makanan Utama",
        "waktu": "3 jam",
        "bahan": "1 kg daging sapi\n1 liter santan kental\n400ml santan encer\n10 buah cabai merah\n8 siung bawang merah\n5 siung bawang putih\n3 batang serai\n5 lembar daun jeruk\n3 lembar daun salam\n2 ruas lengkuas\nGaram dan gula",
        "langkah": "1. Haluskan cabai, bawang, lengkuas.\n2. Tumis bumbu dengan serai, daun jeruk, daun salam.\n3. Masukkan daging, aduk rata.\n4. Tuang santan encer, masak hingga menyusut.\n5. Tuang santan kental, masak terus sampai mengental dan berminyak.\n6. Koreksi rasa, sajikan.",
        "rating": 5,
        "catatan": "Makin lama diaduk, makin awet. Sabar itu kunci rendang.",
    },
    {
        "nama": "Soto Ayam Lamongan",
        "kategori": "Berkuah",
        "waktu": "60 menit",
        "bahan": "1 ekor ayam kampung\n2 liter air\n3 batang serai\n3 lembar daun jeruk\n2 lembar daun salam\n5 siung bawang merah\n3 siung bawang putih\n2 ruas kunyit\n1 ruas jahe\nGaram, merica\nSoun, kol, telur rebus, bawang goreng",
        "langkah": "1. Rebus ayam sampai empuk, angkat, suwir.\n2. Tumis bumbu halus dengan serai, daun jeruk, salam.\n3. Masukkan ke kuah kaldu, didihkan.\n4. Tata soun, kol, telur, ayam suwir di mangkuk.\n5. Siram kuah panas.\n6. Taburi bawang goreng, sajikan dengan nasi.",
        "rating": 4,
        "catatan": "Ayam kampung lebih gurih, tapi ayam broiler lebih cepat empuk.",
    },
    {
        "nama": "Gado-Gado Betawi",
        "kategori": "Sayuran",
        "waktu": "30 menit",
        "bahan": "100g tauge\n100g kangkung\n100g kol\n2 buah tahu, goreng\n1 buah tempe, goreng\n2 butir telur rebus\n100g kacang tanah goreng\n3 siung bawang putih\n5 buah cabai\n2 sdm kecap manis\nGaram, gula merah\nKerupuk",
        "langkah": "1. Rebus sayuran bergantian, tiriskan.\n2. Haluskan kacang, bawang, cabai, gula merah, garam.\n3. Tambahkan air dan kecap, aduk bumbu kacang.\n4. Tata sayuran, tahu, tempe, telur di piring.\n5. Siram bumbu kacang.\n6. Taburi kerupuk, sajikan.",
        "rating": 4,
        "catatan": "Bumbu kacang boleh dicampur kentang rebus biar lebih lembut.",
    },
    {
        "nama": "Bakso Sapi Kenyal",
        "kategori": "Berkuah",
        "waktu": "40 menit",
        "bahan": "500g daging sapi giling\n100g tepung tapioka\n3 siung bawang putih, haluskan\n1 sdt baking powder\nGaram, merica, kaldu bubuk\n2 liter air untuk kuah\nMie kuning, sawi, bawang goreng",
        "langkah": "1. Campur daging, tepung, bawang, baking powder, garam, merica.\n2. Uleni sampai kalis, diamkan 15 menit.\n3. Didihkan air, bentuk bulatan bakso, masukkan ke air.\n4. Masak sampai bakso mengapung.\n5. Rebus mie dan sawi, tata di mangkuk.\n6. Siram kuah, taburi bawang goreng.",
        "rating": 4,
        "catatan": "Aduk satu arah biar serat daging nggak rusak.",
    },
    {
        "nama": "Tempe Mendoan",
        "kategori": "Camilan",
        "waktu": "15 menit",
        "bahan": "1 papan tempe, iris tipis lebar\n100g tepung terigu\n2 sdm tepung beras\n2 siung bawang putih\n1 sdt ketumbar\n1 batang daun bawang, iris\nGaram, air\nMinyak goreng",
        "langkah": "1. Haluskan bawang putih, ketumbar, garam.\n2. Campur tepung, bumbu halus, daun bawang, air jadi adonan encer.\n3. Celup tempe ke adonan.\n4. Goreng sebentar (setengah matang), angkat.\n5. Sajikan dengan sambal kecap.",
        "rating": 5,
        "catatan": "Goreng setengah matang itu ciri mendoan, jangan sampai kering.",
    },
    {
        "nama": "Pisang Goreng Crispy",
        "kategori": "Camilan",
        "waktu": "20 menit",
        "bahan": "5 buah pisang kepok\n150g tepung terigu\n2 sdm tepung beras\n1 sdm gula pasir\n1/2 sdt garam\n1/2 sdt baking powder\nAir secukupnya\nMinyak goreng",
        "langkah": "1. Campur semua bahan kering.\n2. Tuang air sedikit demi sedikit, aduk sampai adonan licin.\n3. Kupas pisang, celup ke adonan.\n4. Goreng di minyak panas sampai keemasan.\n5. Tiriskan, sajikan hangat.",
        "rating": 4,
        "catatan": "Pisang kepok paling pas, jangan pakai pisang ambon (terlalu lembek).",
    },
    {
        "nama": "Es Teh Manis Jumbo",
        "kategori": "Minuman",
        "waktu": "5 menit",
        "bahan": "2 kantong teh celup\n500ml air panas\n3 sdm gula pasir\nEs batu secukupnya\n1 iris lemon (opsional)",
        "langkah": "1. Seduh teh dengan air panas, diamkan 5 menit.\n2. Angkat kantong teh, tambahkan gula, aduk.\n3. Saring ke gelas berisi es batu.\n4. Tambahkan irisan lemon, sajikan.",
        "rating": 5,
        "catatan": "Gula pasir lebih enak dari gula batu buat es teh.",
    },
    {
        "nama": "Sambal Bawang",
        "kategori": "Sambal",
        "waktu": "10 menit",
        "bahan": "15 buah cabai rawit merah\n5 siung bawang putih\n3 siung bawang merah\n1 buah tomat kecil\n1 sdt garam\n1 sdt gula pasir\n5 sdm minyak panas",
        "langkah": "1. Ulek kasar cabai, bawang, tomat, garam, gula.\n2. Panaskan minyak sampai berasap.\n3. Siram minyak panas ke sambal, aduk rata.\n4. Sajikan sebagai pelengkap.",
        "rating": 5,
        "catatan": "Minyak harus benar-benar panas biar sambal wangi.",
    },
]


def seed():
    app = create_app()
    with app.app_context():
        # Cari user pertama sebagai author
        author = User.query.first()
        if not author:
            print("[!] Belum ada user. Bikin user dummy 'demo'...")
            author = User(username="demo")
            author.set_password("demo12345")
            db.session.add(author)
            db.session.commit()
            print(f"[+] User 'demo' dibuat (password: demo12345)")

        added = 0
        skipped = 0
        for r in RECIPES:
            exists = Recipe.query.filter_by(nama=r["nama"]).first()
            if exists:
                skipped += 1
                continue
            recipe = Recipe(user_id=author.id, **r)
            db.session.add(recipe)
            added += 1

        db.session.commit()
        print(f"[✓] Selesai. {added} resep ditambah, {skipped} dilewati (sudah ada).")
        print(f"    Total resep di DB: {Recipe.query.count()}")
        print(f"    Author: {author.username}")


if __name__ == "__main__":
    seed()