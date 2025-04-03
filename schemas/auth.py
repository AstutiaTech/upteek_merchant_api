from pydantic import BaseModel
from typing import Optional, Any

class LoginEmailRequest(BaseModel):
    email: str
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

