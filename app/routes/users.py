from fastapi import APIRouter, status

from app.controllers.user_controller import (
    create_user,
    create_admin,
)

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    AdminRegisterRequest,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# --------------------------------------------------
# Register Customer
# --------------------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: UserCreate):
    """
    Register a new customer.
    """
    return create_user(user)


# --------------------------------------------------
# Register Admin
# --------------------------------------------------
@router.post(
    "/register-admin",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_admin(admin: AdminRegisterRequest):
    """
    Register a new administrator.

    Requires a valid admin registration key.
    """
    return create_admin(admin)