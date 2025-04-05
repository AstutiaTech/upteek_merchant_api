from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_product, update_product, delete_product, get_products, get_single_product_by_id
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate