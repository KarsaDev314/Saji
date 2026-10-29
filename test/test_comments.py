from flask import url_for
from core.db_models import Recipe

def test_add_comment(client, app):
    # 1. Login & Bikin Resep (PAKAI /recipes/new)
    client.post('/login', data={'username': 'kyotest', 'password': 'password123'})
    client.post('/recipes/new', data={
        'nama': 'Resep Tes Komentar', 'kategori': 'Makanan Utama', 'waktu': '10 menit',
        'bahan': 'Nasi', 'langkah': 'Masak'
    }, follow_redirects=True)
    
    # 2. Cari ID asli dari database
    with app.app_context():
        resep = Recipe.query.filter_by(nama='Resep Tes Komentar').first()
        assert resep is not None, "Resep gagal dibuat!"
        resep_id = resep.id
    
    # 3. Pakai ID asli buat url_for
    with app.test_request_context():
        url_komentar = url_for('tambah_komentar', resep_id=resep_id)
    
    # 4. Kirim Komentar
    response = client.post(url_komentar, data={
        'teks': 'Wah, resepnya mantap banget Kyo!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Wah, resepnya mantap banget Kyo!' in response.data