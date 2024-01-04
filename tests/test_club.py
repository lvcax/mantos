import factory

from mantos.models import Club
from mantos.utils import generate_club, generate_country


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


def test_create_club_already_exist(client, club):
    response = client.post(
        '/clubs/', json={'name': 'Milan', 'country': 'Italy'}
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'club already exists'}


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
            club: Club = Club(name=club_name, country=generate_country())

            clubs.append(club)
            last_club_name = club_name
            count += 1

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs')

    assert response.status_code == 200
    assert len(response.json()['clubs']) == 5


def test_list_clubs_pagination(session, client):
    last_club_name = generate_club()
    count = 0
    clubs = list()

    while count < 8:
        club_name = generate_club()

        if club_name != last_club_name:
            club: Club = Club(name=club_name, country=generate_country())

            clubs.append(club)
            last_club_name = club_name
            count += 1

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs/?offset=1&limit=4')

    assert len(response.json()['clubs']) == 4


def test_list_clubs_filter_by_country(session, client):
    last_club_name = generate_club()
    count = 0
    clubs = list()

    while count < 3:
        club_name = generate_club()

        if club_name != last_club_name:
            club: Club = Club(name=club_name, country='Brazil')

            clubs.append(club)
            last_club_name = club_name
            count += 1

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs/?country=Brazil')

    assert len(response.json()['clubs']) == 3


def test_list_clubs_filter_by_country_error(session, client):
    last_club_name = generate_club()
    count = 0
    clubs = list()

    while count < 3:
        club_name = generate_club()

        if club_name != last_club_name:
            club: Club = Club(name=club_name, country='Brazil')

            clubs.append(club)
            last_club_name = club_name
            count += 1

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs/?country=Alemanha')

    assert response.json() == {'detail': 'invalid country name'}


def test_list_clubs_filter_by_name(session, client):
    last_club_name = generate_club()
    count = 0
    clubs = list()

    while count < 5:
        club_name = generate_club()

        if club_name != last_club_name:
            club: Club = Club(name=club_name, country=generate_country())

            clubs.append(club)
            last_club_name = club_name
            count += 1

    club: Club = Club(name='Real Madrid', country='Spain')
    clubs.append(club)

    session.bulk_save_objects(objects=clubs)

    response = client.get('/clubs/?name=Real Madrid')

    assert response.status_code == 200
    assert len(response.json()['clubs']) == 1
