from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Request schema for user login.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Response schema returned after successful login.
    """

    access_token: str
    token_type: str 


class TokenPayload(BaseModel):
    """
    Internal schema representing the decoded JWT payload.
    """

    sub: str
    role: str