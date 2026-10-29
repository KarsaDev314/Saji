from core.db_models import Recipe

def test_search_and_filter(client, app):
    client.post('/login', data={'username': 'kyotest', 'password': 'password123'})
    
    # PAKAI /recipes/new
    client.post('/recipes/new', data={'nama': 'Nasi Goreng', 'kategori': 'Makanan Utama', 'waktu': '10 menit', 'bahan': 'Nasi', 'langkah': 'Goreng'}, follow_redirects=True)
    client.post('/recipes/new', data={'nama': 'Es Teh Manis', 'kategori': 'Minuman', 'waktu': '5 menit', 'bahan': 'Teh', 'langkah': 'Seduh'}, follow_redirects=True)
    
    # Pastiin resepnya beneran masuk ke DB
    with app.app_context():
        assert Recipe.query.filter_by(nama='Nasi Goreng').first() is not None
        assert Recipe.query.filter_by(nama='Es Teh Manis').first() is not None
    
    # 1. Tes Pencarian
    response = client.get('/?q=Nasi&mode=explore')
    assert b'Nasi Goreng' in response.data
    assert b'Es Teh Manis' not in response.data 
    
    # 2. Tes Filter Kategori
    response_kat = client.get('/?kategori=Minuman&mode=explore')
    assert b'Es Teh Manis' in response_kat.data
    assert b'Nasi Goreng' not in response_kat.data