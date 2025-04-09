from fastapi import APIRouter, Request, Depends
from modules.miscelleanous.geo import retrieve_countries, retrieve_single_country, retrieve_single_country_by_code, retrieve_currencies, retrieve_single_currency, retrieve_single_currency_by_code, retrieve_states, retrieve_single_state, retrieve_cities, retrieve_single_city, retrieve_lgas, retrieve_single_lga
from database.schema import ErrorResponse, CountryModel, CountryResponseModel, CurrencyModel, CurrencyResponseModel, StateModel, StateResponseModel, CityModel, CityResponseModel, LGAModel, LGAResponseModel
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import Page

router = APIRouter(
    prefix="/geo",
    tags=["geo"]
)

@router.get("/countries", response_model=Page[CountryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def countries(request: Request, db: Session = Depends(get_session)):
    return retrieve_countries(db=db)


@router.get("/countries/get_single/{country_id}", response_model=CountryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def countries_get_single(request: Request, db: Session = Depends(get_session), country_id: int = 0):
    return retrieve_single_country(db=db, id=country_id)

@router.get("/countries/get_single_code/{country_code}", response_model=CountryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def countries_get_single(request: Request, db: Session = Depends(get_session), country_code: str = None):
    return retrieve_single_country_by_code(db=db, code=country_code)

@router.get("/currencies", response_model=Page[CurrencyModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def currencies(request: Request, db: Session = Depends(get_session)):
    return retrieve_currencies(db=db)

@router.get("/currencies/get_single/{currency_id}", response_model=CurrencyResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def currencies_get_single(request: Request, db: Session = Depends(get_session), currency_id: int = 0):
    return retrieve_single_currency(db=db, currency_id=currency_id)

@router.get("/currencies/get_single_code/{currency_code}", response_model=CurrencyResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def currencies_get_single(request: Request, db: Session = Depends(get_session), currency_code: str = None):
    return retrieve_single_currency_by_code(db=db, code=currency_code)

@router.get("/states", response_model=Page[StateModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def states(request: Request, db: Session = Depends(get_session), country_id: int = 0):
    filters = {}
    if country_id is not None and country_id > 0:
        filters['country_id'] = country_id
    return retrieve_states(db=db, filters=filters)

@router.get("/states/get_single/{state_id}", response_model=StateResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def states_get_single(request: Request, db: Session = Depends(get_session), state_id: int = 0):
    return retrieve_single_state(db=db, state_id=state_id)

@router.get("/cities", response_model=Page[CityModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def cities(request: Request, db: Session = Depends(get_session), state_id: int = 0):
    filters = {}
    if state_id is not None and state_id > 0:
        filters['state_id'] = state_id
    return retrieve_cities(db=db, filters=filters)

@router.get("/cities/get_single/{city_id}", response_model=CityResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def cities_get_single(request: Request, db: Session = Depends(get_session), city_id: int = 0):
    return retrieve_single_city(db=db, city_id=city_id)

@router.get("/lgas", response_model=Page[LGAModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def lgas(request: Request, db: Session = Depends(get_session), state_id: int = 0):
    filters = {}
    if state_id is not None and state_id > 0:
        filters['state_id'] = state_id
    return retrieve_lgas(db=db, filters=filters)

@router.get("/lgas/get_single/{lga_id}", response_model=LGAResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def lgas_get_single(request: Request, db: Session = Depends(get_session), lga_id: int = 0):
    return retrieve_single_lga(db=db, lga_id=lga_id)

