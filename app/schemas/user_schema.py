from app.schemas import order_schema
from pydantic import BaseModel,EmailStr,Field 

class UserCreate(BaseModel):
    """
    Schema used when registering a new user
    """

    username:str
    email:EmailStr
    password:str



class UserResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id:int
    username:str
    email:EmailStr
    role:str
    is_active:bool


class UserUpdate(BaseModel):
    """
    Schema used for updating
    """
    username:str
    email:EmailStr


class AdminRegisterRequest(UserCreate):
    """
    Request schema for admin registration.
    """

    admin_key: str

class UserUpdate(BaseModel):
    """
    Schema used for updating the current user's profile.
    """
    username:str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username",
    )

    email:EmailStr = Field(
        ...,
        description="User email address"
    )