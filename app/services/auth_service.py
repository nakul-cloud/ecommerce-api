from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt_handler import create_access_token
from app.auth.password import verify_password
from app.config.database import get_db_connection
from app.exceptions.custom_exceptions import InvalidCredentialsException
from app.schemas.auth_schema import TokenResponse


def login_user(
    form_data: OAuth2PasswordRequestForm,
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            hashed_password,
            role,
            is_active
        FROM users
        WHERE email = ?
        """,
        (form_data.username,),
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise InvalidCredentialsException()

    if not verify_password(
        form_data.password,
        user["hashed_password"],
    ):
        raise InvalidCredentialsException()

    if not user["is_active"]:
        raise InvalidCredentialsException()

    access_token = create_access_token(
        data={
            "sub": user["email"],
            "role": user["role"],
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
