from typing import Dict, List
from sqlalchemy.orm import Session
from database.model import create_product, update_product, delete_product, get_products, get_single_product_by_id, create_medium_pivot
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate

def create_new_product(db: Session, user_id: int=0, merchant_id: int=0, category_id: int=0, currency_id: int=0, name: str=None, description: str=None, units: int=0, price: float=0, discount: float=0, special_note: str=None, unit_low_level: int=0, media: List=[]):
    product = create_product(db=db, merchant_id=merchant_id, category_id=category_id, currency_id=currency_id, name=name, description=description, units=units, price=price, discount=discount, special_note=special_note, unit_low_level=unit_low_level, status=1, created_by=user_id)
    if media != []:
        for medium in media:
            create_medium_pivot(db=db, medium_id=medium['id'], mediumable_type='product', mediumable_id=product.id, status=1)
    
