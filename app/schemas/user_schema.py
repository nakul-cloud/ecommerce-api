from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.validators import (
    strip_whitespace,
    lowercase_email,
    prevent_empty,
    validate_password_strength,
)


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

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return prevent_empty(strip_whitespace(v))

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return lowercase_email(strip_whitespace(v))

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)


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

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return prevent_empty(strip_whitespace(v))

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return lowercase_email(strip_whitespace(v))


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
# Register Warehouse User
# --------------------------------------------------

class WarehouseRegisterRequest(UserCreate):
    """
    Schema used when an admin registers a warehouse staff member.
    No secret key required — route is protected by require_role(ADMIN).
    """
    pass


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

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)