from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import jwt
from src.core.database import SessionLocal
from src.core.model import User
from src.core.config import config
from riotwatcher import LolWatcher, RiotWatcher


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/auth/signin-form-data", scheme_name="JWT")


def get_logged_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, config.jwt_access_secret_key, algorithms=[config.jwt_algorithm])
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db.query(User).filter(User.id == payload["sub"]).first()


def get_logged_admin(logged_user: User = Depends(get_logged_user)):
    if not logged_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access allowed only for administrators")
    return logged_user


def get_riot_watcher():
    return RiotWatcher(config.riot_api_key)


def get_lol_watcher():
    return LolWatcher(config.riot_api_key)
