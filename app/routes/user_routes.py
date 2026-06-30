from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.controllers.user_controller import UserController
from app.schemas.user_schema import (
    AdminRegisterRequest,
    ChangePasswordRequest,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register")
def store(user: UserCreate):
    """
    Register a new customer.
    """
    return UserController.store(user)


@router.post("/register-admin")
def store_admin(admin: AdminRegisterRequest):
    """
    Register a new administrator.
    """
    return UserController.store_admin(admin)


@router.get(
    "/me",
    summary="Get current user profile",
)
def show(
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve the profile of the currently authenticated user.
    """
    return UserController.show(current_user)


@router.put(
    "/me",
    summary="Update current user profile",
)
def update(
    user: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Update the profile of the currently authenticated user.
    """
    return UserController.update(
        current_user=current_user,
        user=user,
    )


@router.put(
    "/change-password",
    summary="Change current user password",
)
def change_password(
    password_data: ChangePasswordRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Change the password of the currently authenticated user.
    """
    return UserController.change_password(
        current_user=current_user,
        password_data=password_data,
    )
