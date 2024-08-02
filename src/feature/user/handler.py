from fastapi import APIRouter, Depends
from src.core.model import User
from src.core.dependency import get_logged_user

from .response import UserResponse

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse)
def get_me(logged_user: User = Depends(get_logged_user)):
    return logged_user
