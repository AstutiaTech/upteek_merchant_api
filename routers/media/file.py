from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from typing import List
from modules.authentication.auth import auth
from modules.media.file_upload import upload_file, upload_multiple_files, upload_base64, upload_multiple_base64, update_file, delete_file, retrieve_files, retrieve_single_file
from database.schema import ErrorResponse, PlainResponse, MediumModel, UpdateMediumRequest, MediaResponse, MediaListResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/media",
    tags=["media"]
)


@router.post("/upload", response_model=MediaResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def upload(request: Request, file: UploadFile = File(...), user=Depends(auth.auth_wrapper), db: Session = Depends(get_session)):
    req = upload_file(db=db, file=file, user_id=user['id'], merchant_id=user['merchant_id'])
    return req

@router.post("/upload_multiple", response_model=MediaResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def upload_multiple(request: Request, files: List[UploadFile] = File(...), user=Depends(auth.auth_wrapper), db: Session = Depends(get_session)):
    req = upload_multiple_files(db=db, files=files, user_id=user['id'], merchant_id=user['merchant_id'])
    return req

@router.post("/update/{medium_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateMediumRequest, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), medium_id: int=0):
    values = fields.model_dump()
    req = update_file(db=db, id=medium_id, values=values)
    return req

@router.get("/delete/{medium_id}", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), medium_id: int = 0):
    return delete_file(db=db, id=medium_id)


@router.get("/get_all", response_model=Page[MediumModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session)):
    filters = request.query_params._dict
    filters['merchant_id'] = user['merchant_id']
    return retrieve_files(db=db, filters=filters)

@router.get("/get_single/{medium_id}", response_model=MediumModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_session), medium_id: int = 0):
    return retrieve_single_file(db=db, id=medium_id)
