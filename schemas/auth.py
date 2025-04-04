from pydantic import BaseModel, EmailStr
from typing import Optional, Any

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    phone_number: str
    password: str
    first_name: str
    other_name: Optional[str] = None
    last_name: str
    merchant_name: str
    fbt: Optional[str] = None
    
    class Config:
        orm_mode = True

class LoginEmailRequest(BaseModel):
    email: EmailStr
    password: str
    fbt: Optional[str] = None
    
    class Config:
        orm_mode = True

class SendEmailTokenRequest(BaseModel):
    email: str
    
    class Config:
        orm_mode = True

class FinalisePasswordLessRequest(BaseModel):
    email: str
    token_str: str
    fbt: Optional[str] = None
    
    class Config:
        orm_mode = True

class VerifyEmailTokenRequest(BaseModel):
    email: str
    token_str: str
    
    class Config:
        orm_mode = True

