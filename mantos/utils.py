from pycountry import countries


def search_country(country: str) -> bool:
    if countries.get(name=country) or countries.get(common_name=country):
        return True
    
    return False