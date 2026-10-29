def test_register_and_login(client):
    # 1. Tes Register
    response = client.post('/register', data={
        'username': 'kyotest',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Pastiin setelah register, dia diarahin ke halaman login atau langsung masuk
    
    # 2. Tes Login
    response = client.post('/login', data={
        'username': 'kyotest',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Cek apakah username muncul di navbar (artinya sukses login)
    assert b'kyotest' in response.data