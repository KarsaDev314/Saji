import config

def validate_recipe(form):
    """Validasi form tambah/edit resep."""
    nama = form.get("nama", "").strip()
    kategori = form.get("kategori", "").strip()
    waktu = form.get("waktu", "").strip()

    if not nama:
        return None, "Nama resep wajib diisi."
    if len(nama) > config.MAX_NAMA:
        return None, f"Nama resep maksimal {config.MAX_NAMA} karakter."
    if len(waktu) > config.MAX_WAKTU:
        return None, f"Waktu maksimal {config.MAX_WAKTU} karakter."
    if kategori not in config.KATEGORI_VALID:
        kategori = "Lain-lain"

    bahan = [b.strip() for b in form.get("bahan", "").split("\n") if b.strip()]
    langkah = [l.strip() for l in form.get("langkah", "").split("\n") if l.strip()]

    if len(bahan) > config.MAX_BAHAN_COUNT:
        return None, f"Bahan maksimal {config.MAX_BAHAN_COUNT} item."
    if len(langkah) > config.MAX_LANGKAH_COUNT:
        return None, f"Langkah maksimal {config.MAX_LANGKAH_COUNT} item."
    if any(len(b) > config.MAX_BAHAN_ITEM for b in bahan):
        return None, f"Satu bahan maksimal {config.MAX_BAHAN_ITEM} karakter."
    if any(len(l) > config.MAX_LANGKAH_ITEM for l in langkah):
        return None, f"Satu langkah maksimal {config.MAX_LANGKAH_ITEM} karakter."

    return {
        "nama": nama, "kategori": kategori, "waktu": waktu or "-",
        "bahan": bahan, "langkah": langkah,
    }, None

def validate_username_format(username):
    if not username:
        return "Username wajib diisi."
    if len(username) < 3:
        return "Username minimal 3 karakter."
    if len(username) > 30:
        return "Username maksimal 30 karakter."
    if " " in username:
        return "Username tidak boleh ada spasi."
    return None

def validate_registration(username, password, password2):
    err = validate_username_format(username)
    if err:
        return err
    if len(password) < 6:
        return "Password minimal 6 karakter."
    if password != password2:
        return "Konfirmasi password tidak cocok."
    return None

def validate_bio(bio):
    if len(bio) > 300:
        return "Bio maksimal 300 karakter."
    return None