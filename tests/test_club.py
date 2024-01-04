def test_create_club(client):
    response = client.post(
        '/clubs/', json={'name': 'Vasco da Gama', 'country': 'Brazil'}
    )

    assert response.status_code == 201
    assert response.json()['name'] == 'Vasco da Gama'
    assert response.json()['country'] == 'Brazil'
    assert 'id' in response.json()


def test_create_club_with_wrong_country_name(client):
    response = client.post(
        '/clubs/', json={'name': 'Vasco da Gama', 'country': 'Brasil'}
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'invalid country name'}
