from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.inventories.categories import create_new_category, update_existing_category, delete_exiting_category, retrieve_categories, retrieve_single_category
from database.schema import ErrorResponse, PlainResponse, CreateCategoryRequest, UpdateCategoryRequest, CategoryModel, CategoryResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/inventory/categories",
    tags=["inventory_category"]
)

@router.post("/create", response_model=CategoryResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateCategoryRequest, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session)):
    req = create_new_category(db=db, user_id=user['id'], merchant_id=user['merchant_id'], category_id=fields.category_id, name=fields.name, description=fields.description)
    return req

@router.post("/update/{category_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateCategoryRequest, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), category_id: int=0):
    values = fields.model_dump()
    req = update_existing_category(db=db, id=category_id, values=values)
    return req


@router.get("/delete/{category_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), category_id: int = 0):
    return delete_exiting_category(db=db, id=category_id)


@router.get("/get_all", response_model=Page[CategoryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), category_id: int = None, name: str = None, status: int = None, created_by: int = None, authorized_by: int = None):
    filters = {}
    if category_id is not None and category_id > 0:
        filters['category_id'] = category_id
    if name is not None:
        filters['name'] = name
    if status is not None and status > 0:
        filters['status'] = status
    if created_by is not None and created_by > 0:
        filters['created_by'] = created_by
    if authorized_by is not None and authorized_by > 0:
        filters['authorized_by'] = authorized_by
    filters['merchant_id'] = user['merchant_id']
    return retrieve_categories(db=db, filters=filters)

@router.get("/get_single/{category_id}", response_model=CategoryResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), category_id: int = 0):
    return retrieve_single_category(db=db, id=category_id)
