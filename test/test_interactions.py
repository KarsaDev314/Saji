from flask import url_for
from core.db_models import Recipe

def test_toggle_like_and_favorite(client, app):
    # 1. Login & Bikin Resep (PAKAI /recipes/new)
    client.post('/login', data={'username': 'kyotest', 'password': 'password123'})
    client.post('/recipes/new', data={
        'nama': 'Resep Tes Interaksi', 'kategori': 'Camilan', 'waktu': '5 menit',
        'bahan': 'Air', 'langkah': 'Rebus'
    }, follow_redirects=True)
    
    # 2. Cari ID asli dari database
    with app.app_context():
        resep = Recipe.query.filter_by(nama='Resep Tes Interaksi').first()
        assert resep is not None, "Resep gagal dibuat!"
        resep_id = resep.id
    
    # 3. Pakai ID asli buat url_for
    with app.test_request_context():
        url_like = url_for('toggle_like', resep_id=resep_id)
        url_fav = url_for('toggle_favorit', resep_id=resep_id)
    
    # 4. Tes Like & Favorite
    response_like = client.post(url_like, follow_redirects=True)
    assert response_like.status_code == 200
    
    response_fav = client.post(url_fav, follow_redirects=True)
    assert response_fav.status_code == 200