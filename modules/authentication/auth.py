from typing import Dict
from fastapi import Request
from database.model import get_single_user_by_email_and_user_type, get_single_user_by_phone_number_and_user_type, get_single_user_by_username_user_type, get_single_user_by_any_main_details, get_single_profile_by_user_id, get_single_setting_by_user_id, update_user, create_token, get_latest_user_token_by_type, update_token_by_user_id_and_token_type, update_token_email, get_latest_user_token_by_type_and_status, get_latest_user_token_by_email_and_status, get_single_user_by_id, update_token, get_single_country_by_code, registration_unique_field_check, create_user_with_relevant_rows, get_single_user_by_phone_number_and_user_type, get_single_user_by_username_user_type, get_single_user_by_email_and_user_type
from modules.utils.net import get_ip_info, process_phone_number
from modules.utils.tools import process_schema_dictionary
from modules.utils.auth import AuthHandler, get_next_few_minutes, check_if_time_as_pass_now
from modules.messaging.email import e_send_token
from sqlalchemy.orm import Session
import random
import datetime
import random
import sys, traceback
from settings.constants import USER_TYPES

auth = AuthHandler()

def register_user(db: Session, username: str = None, email: str = None, phone_number: str = None, password: str = None, first_name: str = None, other_name: str = None, last_name: str = None, merchant_name: str = None, fbt: str=None):
    country = get_single_country_by_code(db=db, code="NG")
    username = str(username).strip().replace(" ", "")
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country.code)
    new_phone = None
    if processed_phone_number['status'] == True:
        new_phone = processed_phone_number['phone_number']
    else:
        new_phone = phone_number
    check = registration_unique_field_check(db=db, phone_number=new_phone, username=username, email=email, user_type=USER_TYPES['merchant']['num'])
    if check['status'] == False:
        return {
            'status': False,
            'message': check['message'],
            'data': None,
        }
    else:
        user = create_user_with_relevant_rows(db=db, country_id=country.id, username=username, email=email, phone_number=new_phone, password=password, device_token=fbt, user_type=USER_TYPES['merchant']['num'], role=USER_TYPES['merchant']['roles']['super']['num'], first_name=first_name, other_name=other_name, last_name=last_name, is_merchant=True, merchant_name=merchant_name)
        payload = {
            'id': user.id,
            'country_id': user.country_id,
            'merchant_id': user.merchant_id,
            'username': user.username,
            'phone_number': user.phone_number,
            'user_type': user.user_type,
            'role': user.role,
        }
        token = auth.encode_token(user=payload, device_token=fbt)
        profile = get_single_profile_by_user_id(db=db, user_id=user.id)
        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
        data = {
            'access_token': token,
            'user': {
                'id': user.id,
                'merchant_id': user.merchant_id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'user_type': user.user_type,
                'role': user.role,
                'is_new_user': True,
            },
            'profile': profile,
            'setting': setting,
        }
        return {
            'status': True,
            'message': 'Login Success',
            'data': data,
        }
    

def login_with_email(db: Session, email: str=None, password: str=None, fbt: str=None):
    try:
        user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
        if user is None:
            return {
                'status': False,
                'message': 'Email not correct',
                'data': None
            }
        else:
            if not auth.verify_password(plain_password=password, hashed_password=user.password):
                return {
                    'status': False,
                    'message': 'Password Incorrect',
                    'data': None
                }
            else:
                if user.status == 0:
                    return {
                        'status': False,
                        'message': 'This account has been locked',
                        'data': None
                    }
                if user.deleted_at is not None:
                    return {
                        'status': False,
                        'message': 'This account has been deactivated',
                        'data': None
                    }
                payload = {
                    'id': user.id,
                    'merchant_id': user.merchant_id,
                    'country_id': user.country_id,
                    'username': user.username,
                    'phone_number': user.phone_number,
                    'user_type': user.user_type,
                    'role': user.role,
                }
                token = auth.encode_token(user=payload, device_token=fbt)
                da = {
                    'device_token': fbt
                }
                update_user(db=db, id=user.id, values=da)
                profile = get_single_profile_by_user_id(db=db, user_id=user.id)
                setting = get_single_setting_by_user_id(db=db, user_id=user.id)
                data = {
                    'access_token': token,
                    'user': {
                        'id': user.id,
                        'merchant_id': user.merchant_id,
                        'username': user.username,
                        'phone_number': user.phone_number,
                        'email': user.email,
                        'user_type': user.user_type,
                        'role': user.role,
                        'is_new_user': False,
                    },
                    'profile': profile,
                    'setting': setting,
                }
                return {
                    'status': True,
                    'message': 'Login Success',
                    'data': data,
                }
    except Exception as e:
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        return {
            'status': False,
            'message': err,
            'data': None
        }

def send_email_token(db: Session, email: str=None):
    update_token_email(db=db, email=email, values={'status': 2})
    minutes = 10
    expired_at = get_next_few_minutes(minutes=minutes)
    token = str(random.randint(100000,999999))
    create_token(db=db, email=email, token_type="email", token_value=token, status=0, expired_at=expired_at)
    e_send_token(username="Upteek User", email=email, token=token, minutes=minutes)
    return {
        'status': True,
        'message': 'Success',
    }
    
def send_user_email_token(db: Session, email: str=None):
    user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
    if user is None:
        return {
            'status': False,
            'message': 'Email not correct',
        }
    else:
        update_token_by_user_id_and_token_type(db=db, user_id=user.id, token_type="email", values={'status': 2})
        minutes = 10
        expired_at = get_next_few_minutes(minutes=minutes)
        token = str(random.randint(100000,999999))
        create_token(db=db, user_id=user.id, email=email, token_type="email", token_value=token, status=0, expired_at=expired_at)
        e_send_token(username=user.username, email=email, token=token, minutes=minutes)
        return {
            'status': True,
            'message': 'Success',
        }

# def finalise_passwordless_login(db: Session, email: str=None, token_str: str=None, fbt: str=None):
#     user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
#     if user is None:
#         return {
#             'status': False,
#             'message': 'Email not correct',
#             'data': None
#         }
#     else:
#         token = get_latest_user_token_by_email_and_status(db=db, email=email, token_type="email", status=0)
#         if token is None:
#             return {
#                 'status': False,
#                 'message': 'User has no pending email token',
#                 'data': None
#             }
#         else:
#             if token.status != 0:
#                 return {
#                     'status': False,
#                     'message': 'Token already used',
#                     'data': None
#                 }
#             if token.token_value != token_str:
#                 return {
#                     'status': False,
#                     'message': 'Invalid Token Value',
#                     'data': None
#                 }
#             if check_if_time_as_pass_now(time_str=token.expired_at) == True:
#                 update_token(db=db, id=token.id, values={'status': 2})
#                 return {
#                     'status': False,
#                     'message': 'Token has expired',
#                     'data': None
#                 }
#             if user.status == 0:
#                 return {
#                     'status': False,
#                     'message': 'This account has been locked',
#                     'data': None
#                 }
#             if user.deleted_at is not None:
#                 return {
#                     'status': False,
#                     'message': 'This account has been deactivated',
#                     'data': None
#                 }
#             payload = {
#                 'id': user.id,
#                 'merchant_id': user.merchant_id,
#                 'country_id': user.country_id,
#                 'username': user.username,
#                 'phone_number': user.phone_number,
#                 'user_type': user.user_type,
#                 'role': user.role,
#             }
#             access_token = auth.encode_token(user=payload, device_token=fbt)
#             da = {
#                 'device_token': fbt
#             }
#             update_user(db=db, id=user.id, values=da)
#             update_token(db=db, id=token.id, values={'status': 1})
#             profile = get_single_profile_by_user_id(db=db, user_id=user.id)
#             setting = get_single_setting_by_user_id(db=db, user_id=user.id)
#             data = {
#                 'access_token': access_token,
#                 'id': user.id,
#                 'merchant_id': user.merchant_id,
#                 'username': user.username,
#                 'phone_number': user.phone_number,
#                 'email': user.email,
#                 'user_type': user.user_type,
#                 'role': user.role,
#                 'profile': profile,
#                 'setting': setting,
#             }
#             return {
#                 'status': True,
#                 'message': 'Login Success',
#                 'data': data,
#             }

def finalise_passwordless_login(db: Session, email: str=None, token_str: str=None, fbt: str=None):
    token = get_latest_user_token_by_email_and_status(db=db, email=email, token_type="email", status=0)
    if token is None:
        return {
            'status': False,
            'message': 'User has no pending email token',
            'data': None
        }
    else:
        if token.status != 0:
            return {
                'status': False,
                'message': 'Token already used',
                'data': None
            }
        if token.token_value != token_str:
            return {
                'status': False,
                'message': 'Invalid Token Value',
                'data': None
            }
        if check_if_time_as_pass_now(time_str=token.expired_at) == True:
            update_token(db=db, id=token.id, values={'status': 2})
            return {
                'status': False,
                'message': 'Token has expired',
                'data': None
            }
        is_new_user = False
        country = get_single_country_by_code(db=db, code="NG")
        user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
        if user is None:
            user = create_user_with_relevant_rows(db=db, country_id=country.id, email=email, device_token=fbt, user_type=USER_TYPES['merchant']['num'], role=USER_TYPES['merchant']['roles']['super']['num'], is_merchant=True)
            is_new_user = True
        if user.status == 0:
            return {
                'status': False,
                'message': 'This account has been locked',
                'data': None
            }
        if user.deleted_at is not None:
            return {
                'status': False,
                'message': 'This account has been deactivated',
                'data': None
            }
        payload = {
            'id': user.id,
            'merchant_id': user.merchant_id,
            'country_id': user.country_id,
            'username': user.username,
            'phone_number': user.phone_number,
            'user_type': user.user_type,
            'role': user.role,
        }
        access_token = auth.encode_token(user=payload, device_token=fbt)
        da = {
            'device_token': fbt
        }
        update_user(db=db, id=user.id, values=da)
        update_token(db=db, id=token.id, values={'status': 1})
        profile = get_single_profile_by_user_id(db=db, user_id=user.id)
        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
        data = {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'merchant_id': user.merchant_id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'user_type': user.user_type,
                'role': user.role,
                'is_new_user': is_new_user,
            },
            'profile': profile,
            'setting': setting,
        }
        return {
            'status': True,
            'message': 'Login Success',
            'data': data,
        }


def verify_email_token(db: Session, email: str=None, token_str: str=None):
    user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
    if user is None:
        return {
            'status': False,
            'message': 'Email not correct',
        }
    else:
        token = get_latest_user_token_by_type_and_status(db=db, user_id=user.id, token_type="email", status=0)
        if token is None:
            return {
                'status': False,
                'message': 'User has no pending email token',
            }
        else:
            if token.status != 0:
                return {
                    'status': False,
                    'message': 'Token already used',
                }
            if token.token_value != token_str:
                return {
                    'status': False,
                    'message': 'Invalid Token Value',
                }
            if check_if_time_as_pass_now(time_str=token.expired_at) == True:
                update_token(db=db, id=token.id, values={'status': 2})
                return {
                    'status': False,
                    'message': 'Token has expired',
                }
            update_token(db=db, id=token.id, values={'status': 1})
            return {
                'status': True,
                'message': 'Success'
            }

def get_user_details(db: Session, user_id: int=0):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        profile = get_single_profile_by_user_id(db=db, user_id=user.id)
        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
        data = {
            'user': {
                'id': user.id,
                'merchant_id': user.merchant_id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'user_type': user.user_type,
                'role': user.role,
                'is_new_user': False,
            },
            'profile': profile,
            'setting': setting,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }

def check_if_phone_number_exists(db: Session, phone_number: str=None):
    country = get_single_country_by_code(db=db, code="NG")
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country.code)
    new_phone = None
    if processed_phone_number['status'] == True:
        new_phone = processed_phone_number['phone_number']
    else:
        new_phone = phone_number
    phone_number_check = get_single_user_by_phone_number_and_user_type(db=db, phone_number=new_phone, user_type=USER_TYPES['merchant']['num'])
    if phone_number_check is not None:
        return {
            'status': True,
            'message': 'Phone number already exist',
        }
    else:
        return {
            'status': False,
            'message': 'Phone does not exist',
        }
        
def check_if_username_exists(db: Session, username: str=None):
    username_check = get_single_user_by_username_user_type(db=db, username=username, user_type=USER_TYPES['merchant']['num'])
    if username_check is not None:
        return {
            'status': True,
            'message': 'Username already exists'
        }
    else:
        return {
            'status': False,
            'message': 'Username does not exists'
        }
    

def check_if_email_exists(db: Session, email: str=None):
    email_check = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['merchant']['num'])
    if email_check is not None:
        return {
            'status': True,
            'message': 'Email already exists'
        }
    else:
        return {
            'status': False,
            'message': 'Email does not exists'
        }
    

# async def sso_google(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = token.get('userinfo')
