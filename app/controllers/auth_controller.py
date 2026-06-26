from app.config.database import get_db_connection

from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
)

from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token
from app.exceptions.custom_exceptions import InvalidCredentialsException



def login_user(login_data: LoginRequest) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.
    """

    # Create database connection
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # --------------------------------------------------
    # Find user by email
    # --------------------------------------------------
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
        (login_data.email,),
    )

    user = cursor.fetchone()

    # Close connection
    conn.close()

    # --------------------------------------------------
    # User does not exist
    # --------------------------------------------------
    if user is None:
        raise InvalidCredentialsException
    # --------------------------------------------------
    # Verify password
    # --------------------------------------------------
    if not verify_password(
        login_data.password,
        user["hashed_password"],
    ):
        raise InvalidCredentialsException
        
    # --------------------------------------------------
    # Generate JWT
    # --------------------------------------------------
    access_token = create_access_token(
        data={
            "sub": user["email"],
            "role": user["role"],
        }
    )

    # --------------------------------------------------
    # Return token
    # --------------------------------------------------
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )