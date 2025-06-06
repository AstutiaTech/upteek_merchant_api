from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_category, update_category, delete_category, get_categories,get_single_category_by_id
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate

def create_new_category(db: Session, user_id: int=0, merchant_id: int=0, category_id: int=0, name: str=None, description: str=None):
    category = create_category(db=db, merchant_id=merchant_id, category_id=category_id, name=name, description=description, status=1, created_by=user_id)
    return {
        'status': True,
        'message': 'Success',
        'data': category
    }

def update_existing_category(db: Session, id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_category(db=db, id=id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_exiting_category(db: Session, id: int=0):
    delete_category(db=db, id=id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_categories(db: Session, filters: Dict={}):
    data = get_categories(db=db, filters=filters)
    return paginate(data)

def retrieve_single_category(db: Session, id: int=0):
    category = get_single_category_by_id(db=db, id=id)
    if category is None:
        return {
            'status': False,
            'message': 'Category not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': category
        }