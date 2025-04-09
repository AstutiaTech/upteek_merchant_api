from typing import Optional
from pydantic import BaseModel

class UpdateBasicProfileRequestModel(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    merchant_category_id: Optional[int] = None
    merchant_currency_id: Optional[int] = None
    merchant_name: Optional[str] = None
    merchant_trading_name: Optional[str] = None
    merchant_description: Optional[str] = None
    merchant_email: Optional[str] = None
    merchant_phone_number: Optional[str] = None
    
    class Config:
        orm_mode = True
class UpdatePasswordRequestModel(BaseModel):
    password: str
    old_password: str
    
    class Config:
        orm_mode = True

class UpdateSettingsRequestModel(BaseModel):
    email_notification: Optional[int] = None
    sms_notification: Optional[int] = None
    
    class Config:
        orm_mode = True