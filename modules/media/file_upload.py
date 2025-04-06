from typing import Dict
from sqlalchemy.orm import Session
from fastapi import UploadFile
from database.model import create_medium, update_medium, delete_medium, get_media, get_single_medium_by_id
from modules.utils.files import upload_request_file_to_cloudinary, upload_base64_to_cloudinary
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate

def upload_file(file: UploadFile, db: Session, user_id: int=0, merchant_id: int=0) -> Dict:
    upload_result = upload_request_file_to_cloudinary(file=file)
    if upload_result['status'] == True:
        file_url = upload_result['data']['uploaded_url']
        file_path = upload_result['data']['public_id']
        medium = create_medium(db=db, merchant_id=merchant_id, file_type=file.content_type, file_name=file.filename, file_path=file_path, file_url=file_url, status=1, created_by=user_id)
        return {
            'status': True,
            'message': 'Success',
            'data': medium
        }
    else:
        return {
            'status': False,
            'message': upload_result['message'],
            'data': None
        }

def upload_multiple_files(files: list, db: Session, user_id: int=0, merchant_id: int=0) -> Dict:
    results = []
    for file in files:
        upload_result = upload_request_file_to_cloudinary(file=file)
        if upload_result['status'] == True:
            file_url = upload_result['data']['uploaded_url']
            file_path = upload_result['data']['public_id']
            medium = create_medium(db=db, merchant_id=merchant_id, file_type=file.content_type, file_name=file.filename, file_path=file_path, file_url=file_url, status=1, created_by=user_id)
            results.append(medium)
        else:
            return {
                'status': False,
                'message': upload_result['message'],
                'data': None
            }
    return {
        'status': True,
        'message': 'Success',
        'data': results
    }

def upload_base64(base64_string: str, db: Session, file_type: str = None, file_name: str = None, file_description: str = None) -> Dict:
    upload_result = upload_base64_to_cloudinary(base64_string=base64_string)
    if upload_result['status'] == True:
        file_url = upload_result['data']['uploaded_url']
        file_path = upload_result['data']['public_id']
        medium = create_medium(db=db, file_type=file_type, file_name=file_name, file_description=file_description, file_path=file_path, file_url=file_url, status=1)
        return {
            'status': True,
            'message': 'Success',
            'data': medium
        }
    else:
        return {
            'status': False,
            'message': upload_result['message'],
            'data': None
        }

def upload_multiple_base64(base64_strings: list, db: Session, file_type: str = None, file_name: str = None, file_description: str = None) -> Dict:
    results = []
    for base64_string in base64_strings:
        upload_result = upload_base64_to_cloudinary(base64_string=base64_string)
        if upload_result['status'] == True:
            file_url = upload_result['data']['uploaded_url']
            file_path = upload_result['data']['public_id']
            result = create_medium(db=db, file_type=file_type, file_name=file_name, file_description=file_description, file_path=file_path, file_url=file_url, status=1)
            results.append(result)
        else:
            return {
                'status': False,
                'message': upload_result['message'],
                'data': None
            }
    return {
        'status': True,
        'message': 'Success',
        'data': results
    }

def update_file(db: Session, id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_medium(db=db, id=id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_file(db: Session, id: int=0):
    delete_medium(db=db, id=id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_files(db: Session, filters: Dict={}):
    data = get_media(db=db, filters=filters)
    return paginate(data)

def retrieve_single_file(db: Session, id: int=0):
    file = get_single_medium_by_id(db=db, id=id)
    if file is None:
        return {
            'status': False,
            'message': 'File not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': file
        }
