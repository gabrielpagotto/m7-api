from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.dependency import get_db
from fastapi.security import OAuth2PasswordRequestForm
from src.core.model import User
from src.core.util.password import get_password_hash, is_valid_password
from src.core.util.jwt import create_access_and_refresh_tokens

from .payload import SignupPayload, SigninPayload, RefreshPayload
from .response import AuthenticationResponse

router = APIRouter(prefix="/auth")


@router.post(
    "/signin",
    description="Authenticates the user and returns their access credentials.",
    response_model=AuthenticationResponse,
    tags=["Auth"],
)
async def signin(payload: SigninPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.is_active == True).first()
    if not user or not is_valid_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password is invalid.")

    access_token, refresh_token = create_access_and_refresh_tokens(user)
    return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/signup",
    description="Create a new user and return authorization tokens.",
    response_model=AuthenticationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
)
async def signup(payload: SignupPayload, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email, User.is_active == True).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    hashed_password = get_password_hash(payload.password)
    new_user = User(email=payload.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token, refresh_token = create_access_and_refresh_tokens(new_user)
    return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", description="", response_model=AuthenticationResponse, tags=["Auth"], include_in_schema=False)
async def refresh(payload: RefreshPayload): ...


@router.post("/signin-form-data", include_in_schema=False)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username, User.is_active == True).first()
    if not user or not is_valid_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password is invalid.")

    access_token, refresh_token = create_access_and_refresh_tokens(user)
    return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)
