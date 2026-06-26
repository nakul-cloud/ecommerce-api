from pydantic import BaseModel,EmailStr

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