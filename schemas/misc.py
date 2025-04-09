from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CountryModel(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    code_two: Optional[str] = None
    area_code: Optional[str] = None
    base_timezone: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    flag: Optional[str] = None
    visibility: Optional[int] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CountryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[CountryModel] = None

    class Config:
        orm_mode = True

class CurrencyModel(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    symbol: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CurrencyResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[CurrencyModel] = None

    class Config:
        orm_mode = True

class StateModel(BaseModel):
    id: int
    country_id: Optional[int] = 0
    name: Optional[str] = None
    capital: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class StateResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[StateModel] = None

    class Config:
        orm_mode = True

class CityModel(BaseModel):
    id: int
    state_id: Optional[int] = 0
    name: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_capital: Optional[int] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CityResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[CityModel] = None

    class Config:
        orm_mode = True

class LGAModel(BaseModel):
    id: int
    state_id: Optional[int] = 0
    name: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class LGAResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[LGAModel]

    class Config:
        orm_mode = True

class MerchantIndustryModel(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MerchantIndustryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[MerchantIndustryModel] = None

    class Config:
        orm_mode = True

class MerchantCategoryModel(BaseModel):
    id: int
    industry_id: Optional[int] = 0
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MerchantCategoryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[MerchantCategoryModel] = None

    class Config:
        orm_mode = True