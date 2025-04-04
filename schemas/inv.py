from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CreateCategoryRequest(BaseModel):
    category_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateCategoryRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class CategoryModel(BaseModel):
    id: int
    merchant_id: Optional[int] = 0
    category_id: Optional[int] = 0
    name: str
    description: Optional[str] = None
    status: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CategoryResponse(BaseModel):
    status: bool
    message: str
    data: Optional[CategoryModel] = None

    class Config:
        orm_mode = True