from sqlalchemy.orm import Session
from database.model import create_country


seed = [
    {
        'name': 'Nigeria',
        'code': 'NG',
        'code': 'NGA',
        'language': 'English',
        'area_code': '+234',
        'base_timezone': 'Africa/Lagos',
        'latitude': '9.0820',
        'longitude': '8.6753',
        'flag': 'https://flagicons.lipis.dev/flags/4x3/ng.svg',
        'visibility': 1,
        'status': 1,
    },
    {
        'name': 'Ghana',
        'code': 'GH',
        'code': 'GHA',
        'language': 'English',
        'area_code': '+233',
        'base_timezone': 'Africa/Accra',
        'latitude': '7.9465',
        'longitude': '1.0232',
        'flag': 'https://flagicons.lipis.dev/flags/4x3/gh.svg',
        'visibility': 1,
        'status': 1,
    },
    {
        'name': 'United States',
        'code': 'US',
        'code': 'USA',
        'language': 'English',
        'area_code': '+1',
        'base_timezone': 'America/New_York',
        'latitude': '37.0902',
        'longitude': '-95.7129',
        'flag': 'https://flagicons.lipis.dev/flags/4x3/us.svg',
        'visibility': 1,
        'status': 1,
    },
]

def run_country_seeder(db: Session):
    global seed
    for data in seed:
        create_country(db=db, name=data['name'], code=data['code'], code_two=data['code_two'], language=data['language'], area_code=data['area_code'], base_timezone=data['base_timezone'], latitude=data['latitude'], longitude=data['longitude'], flag=data['flag'], visibility=data['visibility'], status=data['status'])
    return True