import random

import factory

from mantos.models import Club
from mantos.utils import generate_country, generate_club


class ClubFactory(factory.Factory):
    class Meta:
        model = Club

    id = factory.Faker('uuid4')
    name = factory.LazyAttribute(lambda n: generate_club())
    country = factory.LazyAttribute(lambda n: generate_country())


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


def test_list_clubs(session, client):
    last_club_name = generate_club()
    count = 0
    clubs = list()

    while count < 5:
        club_name = generate_club()

        if club_name != last_club_name:
            club: Club = Club(
                name=club_name,
                country=generate_country() 
            )

            clubs.append(club)
            last_club_name = club_name
            count += 1

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs')

    assert response.status_code == 200
    assert len(response.json()['clubs']) == 5
