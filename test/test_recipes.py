from flask import url_for

def test_create_recipe(client, app):
    # 1. Login dulu (wajib, karena tambah resep butuh auth)
    client.post('/login', data={
        'username': 'kyotest',
        'password': 'password123'
    })
    
    # 2. Cari URL tambah resep secara otomatis pakai url_for
    # Ini biar kita nggak salah nebak URL /tambah atau /recipes/tambah
    with app.test_request_context():
        # Kalau nama fungsi route kamu bukan 'tambah', sesuaikan string ini
        url_tambah = url_for('tambah') 
    
    # 3. Tambah Resep
    response = client.post(url_tambah, data={
        'nama': 'Nasi Goreng Test',
        'kategori': 'Makanan Utama',
        'waktu': '15 menit',
        'bahan': 'Nasi\nTelur\nKecap',
        'langkah': 'Goreng nasi\nMasukkan telur'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Cek apakah nama resep muncul di halaman setelah disubmit
    assert b'Nasi Goreng Test' in response.data