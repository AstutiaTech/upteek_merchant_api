from fastapi import APIRouter, Request, Depends, HTTPException
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from modules.authentication.auth import auth, login_with_email, send_email_token, send_user_email_token, finalise_passwordless_login, verify_email_token, get_user_details
from database.schema import ErrorResponse, PlainResponse, PlainResponseData, LoginEmailRequest, SendEmailTokenRequest, FinalisePasswordLessRequest, MainAuthResponseModel, UserResponseModel, VerifyEmailTokenRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login_email", response_model=MainAuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def login_email(request: Request, fields: LoginEmailRequest, db: Session = Depends(get_db)):
    req = login_with_email(db=db, email=fields.email, password=fields.password, fbt=fields.fbt)
    return req

@router.post("/send_token_email", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def send_token_email(request: Request, fields: SendEmailTokenRequest, db: Session = Depends(get_db)):
    req = send_email_token(db=db, email=fields.email)
    return req

@router.post("/send_user_token_email", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def send_user_token_email(request: Request, fields: SendEmailTokenRequest, db: Session = Depends(get_db)):
    req = send_user_email_token(db=db, email=fields.email)
    return req

@router.post("/finalize_passwordless", response_model=MainAuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def finalize_passwordless(request: Request, fields: FinalisePasswordLessRequest, db: Session = Depends(get_db)):
    req = finalise_passwordless_login(db=db, email=fields.email, token_str=fields.token_str, fbt=fields.fbt)
    return req

@router.post("/verify_token_email", response_model=PlainResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def verify_token_email(request: Request, fields: VerifyEmailTokenRequest, db: Session = Depends(get_db)):
    req = verify_email_token(db=db, email=fields.email, token_str=fields.token_str)
    return req

@router.get("/details", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def details(request: Request, user=Depends(auth.auth_wrapper), db: Session = Depends(get_db)):
    return get_user_details(db=db, user_id=user['id'])

