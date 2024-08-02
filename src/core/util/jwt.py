import jwt
from datetime import datetime, timedelta, timezone
from src.core.config import config
from src.core.model import User


def create_access_and_refresh_tokens(user: User):
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt_access_expire_minutes)
    to_encode = dict(exp=expire, sub=str(user.id))
    access_token = jwt.encode(to_encode, config.jwt_access_secret_key, algorithm=config.jwt_algorithm)

    expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt_refresh_expire_minutes)
    to_encode = dict(exp=expire, sub=str(user.id))
    refresh_token = jwt.encode(to_encode, config.jwt_refresh_secret_key, algorithm=config.jwt_algorithm)

    return (access_token, refresh_token)