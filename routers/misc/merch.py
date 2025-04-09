from fastapi import APIRouter, Request, Depends
from modules.miscelleanous.merchant_misc import retrieve_merchant_industries, retrieve_single_merchant_industry, retrieve_merchant_categories, retrieve_single_merchant_category
from database.schema import ErrorResponse, MerchantIndustryModel, MerchantIndustryResponseModel, MerchantCategoryModel, MerchantCategoryResponseModel
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/misc",
    tags=["misc"]
)


@router.get("/industries", response_model=Page[MerchantIndustryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def industries(request: Request, db: Session = Depends(get_session)):
    return retrieve_merchant_industries(db=db)

@router.get("/industries/get_single/{industry_id}", response_model=MerchantIndustryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def industries_get_single(request: Request, db: Session = Depends(get_session), industry_id: int = 0):
    return retrieve_single_merchant_industry(db=db, industry_id=industry_id)

@router.get("/categories", response_model=Page[MerchantCategoryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def categories(request: Request, db: Session = Depends(get_session), industry_id: int = 0):
    filters = {}
    if industry_id is not None and industry_id > 0:
        filters['industry_id'] = industry_id
    return retrieve_merchant_categories(db=db, filters=filters)

@router.get("/categories/get_single/{category_id}", response_model=MerchantCategoryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def categories_get_single(request: Request, db: Session = Depends(get_session), category_id: int = 0):
    return retrieve_single_merchant_category(db=db, category_id=category_id)
