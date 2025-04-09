from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_merchant_industries, get_single_merchant_industry_by_id, get_merchant_categories, get_single_merchant_category_by_id
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_merchant_industries(db: Session):
    industries = get_merchant_industries(db=db)
    return paginate(industries)

def retrieve_single_merchant_industry(db: Session, industry_id: int=0):
    industry = get_single_merchant_industry_by_id(db=db, id=industry_id)
    if industry is None:
        return {
            'status': False,
            'message': 'Merchant Industry not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': industry
        }
    
def retrieve_merchant_categories(db: Session, filters: Dict={}):
    categories = get_merchant_categories(db=db, filters=filters)
    return paginate(categories)

def retrieve_single_merchant_category(db: Session, category_id: int=0):
    category = get_single_merchant_category_by_id(db=db, id=category_id)
    if category is None:
        return {
            'status': False,
            'message': 'Merchant Category not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': category
        }