from typing import Optional
from pydantic import BaseModel

class ProfileModel(BaseModel):
    id: int
    user_id: int
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    mothers_maiden_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    marital_status: Optional[str] = None
    avatar: Optional[str] = None
    id_document_file: Optional[str] = None
    id_document_type: Optional[str] = None
    id_document_value: Optional[str] = None
    selfie: Optional[str] = None
    bvn: Optional[str] = None
    bvn_status: Optional[int] = 0
    nin: Optional[str] = None
    nin_status: Optional[int] = 0
    kyc_level: Optional[int] = 0
    compliance_status: Optional[int] = 0
    
    class Config:
        orm_mode = True

class SettingModel(BaseModel):
    id: int
    user_id: int
    email_notification: Optional[int] = 0
    sms_notification: Optional[int] = 0
    
    class Config:
        orm_mode = True

class AuthResponseModel(BaseModel):
    id: int
    access_token: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    profile: Optional[ProfileModel] = None
    setting: Optional[SettingModel] = None
    
    class Config:
        orm_mode = True

class MainAuthResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AuthResponseModel] = None
    
    class Config:
        orm_mode = True

class UserDetailsResponseModel(BaseModel):
    id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[int] = 0
    role: Optional[int] = 0
    profile: Optional[ProfileModel] = None
    setting: Optional[SettingModel] = None
    
    class Config:
        orm_mode = True

class UserResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserDetailsResponseModel] = None
    
    class Config:
        orm_mode = True
