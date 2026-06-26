from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt_handler import verify_access_token

from app.config.database import get_db_connection

from app.schemas.user_schema import UserResponse

from app.exceptions.custom_exceptions import InvalidTokenException,PermissionDeniedException

from typing import Callable


# --------------------------------------------------
# OAuth2 Scheme
# --------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


# --------------------------------------------------
# Get Current User
# --------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> UserResponse:
    """
    Validate JWT and return the currently authenticated user.
    """

    # Decode JWT
    payload = verify_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise InvalidTokenException()

    # Create database connection
    conn = get_db_connection()

    cursor = conn.cursor()

    # Fetch user
    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            role,
            is_active
        FROM users
        WHERE email = ?
        """,
        (email,),
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        raise InvalidTokenException()

    if not user["is_active"]:
        raise InvalidTokenException()

    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        is_active=bool(user["is_active"]),
    )




def require_role(required_role: str):

    def role_checker(
        current_user: UserResponse = Depends(get_current_user),
    ):

        if current_user.role != required_role:
            raise PermissionDeniedException()

        return current_user

    return role_checker