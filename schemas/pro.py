from typing import Optional
from pydantic import BaseModel

class UpdateBasicProfileRequestModel(BaseModel):
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    
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