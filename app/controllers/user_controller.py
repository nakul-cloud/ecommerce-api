from app.config.database import get_db_connection

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
)
from app.auth.password import hash_password

def create_user(user: UserCreate) -> UserResponse:
    """
    Register a new user.
    """

    # Create database connection
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # --------------------------------------------------
    # Create new user
    # --------------------------------------------------
    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            hashed_password
        )
        VALUES (?, ?, ?)
        """,
        (
            user.username,
            user.email,
            hash_password(user.password),      # Will be hashed in the next step
        ),
    )

    # Save changes
    conn.commit()

    # Get newly created user ID
    user_id = cursor.lastrowid

    # Close connection
    conn.close()

    # Return API response
    return UserResponse(
        id=user_id,
        username=user.username,
        email=user.email,
        role="customer",
        is_active=True,
    )