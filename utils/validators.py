def validate_username_format(username):
    if not username: return "Username wajib diisi."
    if len(username) < 3: return "Username minimal 3 karakter."
    if " " in username: return "Username tidak boleh ada spasi."
    return None