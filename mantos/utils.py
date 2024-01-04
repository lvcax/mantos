import random

from pycountry import countries


def search_country(country: str) -> bool:
    if countries.get(name=country) or countries.get(common_name=country):
        return True
    
    return False


def generate_country() -> str:
    country = random.choice(countries.objects)

    return country.name


def generate_club() -> str:
    clubs = [
        'Vasco da Gama',
        'Barcelona',
        'Arsenal',
        'Corinthians',
        'Boca Juniors',
        'Bahia',
        'Milan',
        'Roma',
        'Orlando Magic',
        'Kashima Antlers',
        'Peñarol',
        'Al Ahly',
        'Porto',
        'CSKA'
    ]

    return random.choice(clubs)
