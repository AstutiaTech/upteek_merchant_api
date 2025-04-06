from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MediumModel(BaseModel):
    id: int
    merchant_id: Optional[int] = 0
    mediumable_type: Optional[str] = None
    mediumable_id: Optional[int] = 0
    file_type: Optional[str] = None
    file_name: Optional[str] = None
    file_description: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    status: Optional[int] = 0
    created_by: Optional[int] = 0
    created_at: datetime

    class Config:
        orm_mode = True

class UpdateMediumRequest(BaseModel):
    file_type: Optional[str] = None
    file_name: Optional[str] = None
    file_description: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class MediaResponse(BaseModel):
    status: bool
    message: str
    data: MediumModel

    class Config:
        orm_mode = True

class MediaListResponse(BaseModel):
    status: bool
    message: str
    data: list[MediumModel]

    class Config:
        orm_mode = True