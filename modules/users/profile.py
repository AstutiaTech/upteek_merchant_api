from typing import Dict
from sqlalchemy.orm import Session
from database.model import update_profile_by_user_id, update_merchant, update_setting_by_user_id, get_single_user_by_id, update_user, get_single_country_by_code
from modules.utils.tools import process_schema_dictionary
from modules.utils.net import process_phone_number
from modules.utils.auth import AuthHandler

auth = AuthHandler()


def update_user_profile_details(db: Session, user_id: int=0, merchant_id: int=0, values: Dict={}):
    country = get_single_country_by_code(db=db, code="NG")
    passvalues = process_schema_dictionary(info=values)
    user_values = {}
    merchant_values = {}
    if 'username' in passvalues:
        username = passvalues.pop('username')
        username = str(username).strip().replace(" ", "")
        user_values['username'] = username
    if 'phone_number' in passvalues:
        phone_number = passvalues.pop('phone_number')
        processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country.code)
        if processed_phone_number['status'] == True:
            user_values['phone_number'] = processed_phone_number['phone_number']
        else:
            user_values['phone_number'] = phone_number
    if 'merchant_category_id' in passvalues:
        merchant_values['category_id'] = passvalues.pop('merchant_category_id')
    if 'merchant_currency_id' in passvalues:
        merchant_values['currency_id'] = passvalues.pop('merchant_currency_id')
    if 'merchant_name' in passvalues:
        merchant_values['name'] = passvalues.pop('merchant_name')
    if 'merchant_trading_name' in passvalues:
        merchant_values['trading_name'] = passvalues.pop('merchant_trading_name')
    if 'merchant_description' in passvalues:
        merchant_values['description'] = passvalues.pop('merchant_description')
    if 'merchant_email' in passvalues:
        merchant_values['email'] = passvalues.pop('merchant_email')
    if 'merchant_phone_number' in passvalues:
        merchant_values['phone_number_one'] = passvalues.pop('merchant_phone_number')
    if user_values != {}:
        update_user(db=db, id=user_id, values=user_values)
    update_profile_by_user_id(db=db, user_id=user_id, values=passvalues)
    if merchant_values != {}:
        update_merchant(db=db, id=merchant_id, values=merchant_values)
    return {
        'status': True,
        'message': 'Success'
    }

def update_user_password(db: Session, user_id: int=0, password: str=None, old_password: str=None):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
        }
    else:
        if auth.verify_password(plain_password=old_password, hashed_password=user.password) == False:
            return {
                'status': False,
                'message': 'Old Password Incorrect'
            }
        else:
            password = auth.get_password_hash(password=password)
            da = {
                'password': password
            }
            update_user(db=db, id=user_id, values=da)
            return {
                'status': True,
                'message': 'Success'
            }

def update_user_settings(db: Session, user_id: int=0, values: Dict={}):
    passvalues = process_schema_dictionary(info=values)
    update_setting_by_user_id(db=db, user_id=user_id, values=passvalues)
    return {
        'status': True,
        'message': 'Success'
    }
