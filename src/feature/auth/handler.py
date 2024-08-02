from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.dependency import get_db, get_logged_user
from src.core.model import User, LeagueOfLegendsAccount
from src.core.util.password import get_password_hash, is_valid_password
from src.core.util.jwt import create_access_and_refresh_tokens

from .payload import SignupPayload, SigninPayload, RefreshPayload
from .response import AuthenticationResponse

router = APIRouter(prefix="/auth")


@router.post(
    "/signin",
    description="Authenticates the user and returns their access credentials.",
    response_model=AuthenticationResponse,
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
)
async def signup(payload: SignupPayload, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == payload.email, User.is_active == True).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    hashed_password = get_password_hash(payload.password)
    new_user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed_password,
        league_of_legends_account=LeagueOfLegendsAccount(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token, refresh_token = create_access_and_refresh_tokens(new_user)
    return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", description="", response_model=AuthenticationResponse)
async def refresh(payload: RefreshPayload): ...


@router.get("/check", dependencies=[Depends(get_logged_user)])
async def only_admin():
    return {"logged": True}
