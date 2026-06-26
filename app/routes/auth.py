from fastapi import APIRouter,status
from app.controllers.auth_controller import login_user

from app.schemas.auth_schema import(
    LoginRequest,
    TokenResponse
)

router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code = status.HTTP_200_OK,
    summary = "user login"
)
def login(login_data: LoginRequest):
    """
    Authenticate a user and return a JWT access token.
    """
    return login_user(login_data)
    