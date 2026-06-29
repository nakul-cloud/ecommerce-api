from pydantic import BaseModel, EmailStr, Field


# --------------------------------------------------
# Register User
# --------------------------------------------------

class UserCreate(BaseModel):
    """
    Schema used when registering a new user.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
    )


# --------------------------------------------------
# User Response
# --------------------------------------------------

class UserResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool


# --------------------------------------------------
# Update Profile
# --------------------------------------------------

class UserUpdate(BaseModel):
    """
    Schema used for updating the current user's profile.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username",
    )

    email: EmailStr = Field(
        ...,
        description="User email address",
    )


# --------------------------------------------------
# Register Admin
# --------------------------------------------------

class AdminRegisterRequest(UserCreate):
    """
    Schema used when registering an administrator.
    """

    admin_key: str = Field(
        ...,
        min_length=5,
    )


# --------------------------------------------------
# Change Password
# --------------------------------------------------

class ChangePasswordRequest(BaseModel):
    """
    Schema used for changing the current user's password.
    """

    old_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Current password",
    )

    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="New password",
    )