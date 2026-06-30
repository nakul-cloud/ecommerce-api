from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.auth_controller import AuthController

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    summary="User Login",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticate a user and return a JWT access token.
    """
    return AuthController.login(form_data)
