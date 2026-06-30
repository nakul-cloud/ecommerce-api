from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service


class AuthController:
    @staticmethod
    def login(
        form_data: OAuth2PasswordRequestForm,
    ) -> dict:
        """
        Authenticate a user and return a JWT access token.
        Conforms to OAuth2 specification by returning the token data at the root level.
        """
        return auth_service.login_user(form_data)
