from fastapi import APIRouter,status
from app.controllers.user_controller import create_user

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

def register_user(user:UserCreate):
    """
    Register a new user.
    """
    return create_user(user)