from sqlalchemy.orm import Session
from database.model import create_currency

seed = [
    {
        'name': 'Naira',
        'code': 'NGN',
        'symbol': '₦',
        'status': 1,
    },
    {
        'name': 'Dollar',
        'code': 'USD',
        'symbol': '$',
        'status': 1,
    },
]

def run_currency_seeder(db: Session):
    global seed
    for data in seed:
        create_currency(db=db, name=data['name'], code=data['code'], symbol=data['symbol'], status=data['status'])
    return True