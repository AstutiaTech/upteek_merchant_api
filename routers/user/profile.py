from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from modules.authentication.auth import auth
from modules.users.profile import update_user_profile_details, update_user_password, update_user_settings
from database.schema import UpdateBasicProfileRequestModel, UpdatePasswordRequestModel, UpdateSettingsRequestModel, ErrorResponse, PlainResponse

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

@router.post("/update", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateBasicProfileRequestModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    values = fields.model_dump()
    req = update_user_profile_details(db=db, user_id=user['id'], values=values)
    return req

@router.post("/update_password", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_password(request: Request, fields: UpdatePasswordRequestModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    req = update_user_password(db=db, user_id=user['id'], password=fields.password, old_password=fields.old_password)
    return req

@router.post("/update_settings", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_password(request: Request, fields: UpdateSettingsRequestModel, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    values = fields.model_dump()
    req = update_user_settings(db=db, user_id=user['id'], values=values)
    return req