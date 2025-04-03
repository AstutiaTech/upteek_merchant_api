from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from database.db import Base, engine
import string 
import random
from datetime import datetime
from typing import List, Dict
from settings.config import load_env_config
import dateparser
import time
import re
import json
import os
import importlib
import pkgutil
import inspect
import models
import traceback

config = load_env_config()

def rand_string_generator(size=10):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def rand_upper_string_generator(size=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
    
def rand_lower_string_generator(size=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def generate_transaction_reference(tran_type: str = None, rand_type: int = 1, rand_size: int = 10):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    if rand_type == 1:
        return str(tran_type).upper() + "_" + rand_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 2:
        return str(tran_type).upper() + "_" + rand_upper_string_generator(size=rand_size) + "_" + str(ts)
    elif rand_type == 3:
        return str(tran_type).upper() + "_" + rand_lower_string_generator(size=rand_size) + "_" + str(ts)

def generate_basic_reference(rand_size: int=10):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    ts = int(ts)
    return rand_upper_string_generator(size=rand_size) + "_" + str(ts)

def process_schema_dictionary(info: Dict={}):
    if bool(info) == False:
        return {}
    else:
        retval = {}
        for i in info:
            if info[i] != None:
                retval[i] = info[i]
        return retval
    
def generate_host_id(first_char: str=None, number: int=0):
    # return first_char + str(number).zfill(9)
    return first_char + rand_upper_string_generator(size=number)

def generate_battery_code(number: int=0, length: int=0):
    return "A87" + str(number).zfill(length) + "P"

def process_datetime_string(time_str: str = None):
    if time_str is None:
        return None
    else:
        return dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    
def slugify(input_string: str=None, strip: str='-'):
    if input_string is None:
        return None
    else:
        input_string = input_string.encode('ascii', 'ignore').decode('ascii').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', input_string)
        slug = slug.strip(strip)
        return slug
    
def is_valid_json(data: str=None):
    try:
        json.loads(data)
        return True
    except Exception as e:
        return False
    
def truncate_table(table_name: str, db: Session):
    """Truncates a given table and resets identity."""
    try:
        db.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        db.commit()
        return {
            'status': True,
            "message": f"Table '{table_name}' truncated successfully!",
        }
    except Exception as e:
        db.rollback()
        return {
            'status': False,
            'message': str(e)
        }
    
# Function to get all table names
def get_all_tables(db: Session):
    inspector = inspect(db.bind)
    return inspector.get_table_names()

# Function to truncate all tables
def truncate_all_tables(db: Session):
    """Truncates all tables in the database."""
    try:
        tables = get_all_tables(db)
        if not tables:
            return {"message": "No tables found in the database!"}

        # Disable foreign key checks (for MySQL) to avoid constraint issues
        db.execute(text("SET session_replication_role = 'replica'"))  # PostgreSQL
        # db.execute(text("SET FOREIGN_KEY_CHECKS=0"))  # Uncomment for MySQL

        for table in tables:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

        # Enable foreign key checks back
        db.execute(text("SET session_replication_role = 'origin'"))  # PostgreSQL
        # db.execute(text("SET FOREIGN_KEY_CHECKS=1"))  # Uncomment for MySQL

        db.commit()
        return {
            "status": True,
            "message": f"All tables truncated successfully: {tables}"
        }

    except Exception as e:
        db.rollback()
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        return {"status": False, "message": err}

# def import_models_from_directory():
#     """
#     Dynamically import all models from the models directory
    
#     This function does the following:
#     1. Walks through the models directory
#     2. Imports all Python modules
#     3. Finds all SQLAlchemy model classes that inherit from Base
#     """
#     model_classes = []
    
#     # Iterate through all modules in the models package
#     for _, module_name, _ in pkgutil.iter_modules(models.__path__):
#         try:
#             # Import the module
#             module = importlib.import_module(f'models.{module_name}')
            
#             # Find all classes in the module that inherit from Base
#             for name, obj in inspect.getmembers(module):
#                 if (inspect.isclass(obj) and 
#                     issubclass(obj, Base) and 
#                     obj is not Base and 
#                     hasattr(obj, '__tablename__')):
#                     model_classes.append(obj)
#         except ImportError as e:
#             print(f"Error importing module {module_name}: {e}")
    
#     return model_classes

# def create_tables():
#     try:
#         # Import all model classes
#         models_to_create = import_models_from_directory()
        
#         # Create all tables
#         Base.metadata.create_all(bind=engine)
        
#         # Return the names of tables that were created
#         return {
#             "status": "success", 
#             "tables_created": [model.__tablename__ for model in models_to_create]
#         }
#     except Exception as e:
#         # Handle any errors during table creation
#         return {
#             "status": "error", 
#             "message": str(e)
#         }