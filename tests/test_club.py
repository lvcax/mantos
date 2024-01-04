def test_create_club(client):
    response = client.post(
        '/clubs/', json={'name': 'Vasco da Gama', 'country': 'Brazil'}
    )

    assert response.status_code == 201
    assert response.json()['name'] == 'Vasco da Gama'
    assert response.json()['country'] == 'Brazil'
    assert 'id' in response.json()
