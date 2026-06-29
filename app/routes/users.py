from fastapi import APIRouter, status,Depends
from app.auth.dependencies import get_current_user

from app.controllers.user_controller import (
    create_user,
    create_admin,
    update_current_user,
    change_password,
)

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    AdminRegisterRequest,
    UserUpdate,
    ChangePasswordRequest,
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


# -----------------------------------------------
# Get Users Profiles
# -----------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
)
def get_my_profile(
    current_user: UserResponse =Depends(get_current_user),

):
    """
    Retrieve the profile of the currently authenticated user.
    """
    return current_user

# --------------------------------------------------
# Update Current User Profile 
# --------------------------------------------------

@router.put(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
)

def update_my_profile(
    user:UserUpdate,
    current_user:UserResponse = Depends(get_current_user),
):
    """
    Update the profile of the currently authenticated user.
    """
    return update_current_user(
        current_user = current_user,
        user=user,
    )

# --------------------------------------------------
# Change Password
# --------------------------------------------------

@router.put(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change current user password",
)
def change_my_password(
    password_data: ChangePasswordRequest,
    current_user: UserResponse = Depends(
        get_current_user,
    ),
):
    """
    Change the password of the currently authenticated user.
    """

    return change_password(
        current_user=current_user,
        password_data=password_data,
    )