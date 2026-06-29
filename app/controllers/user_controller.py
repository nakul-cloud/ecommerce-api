from app.config.database import get_db_connection
from app.config.settings import ADMIN_REGISTRATION_KEY

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    AdminRegisterRequest,
)

from app.auth.password import hash_password

from app.exceptions.custom_exceptions import (
    PermissionDeniedException,
)


# --------------------------------------------------
# Register Customer
# --------------------------------------------------

def create_user(user: UserCreate) -> UserResponse:
    """
    Register a new customer.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

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
            hash_password(user.password),
        ),
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return UserResponse(
        id=user_id,
        username=user.username,
        email=user.email,
        role="customer",
        is_active=True,
    )


# --------------------------------------------------
# Register Admin
# --------------------------------------------------

def create_admin(admin: AdminRegisterRequest) -> UserResponse:
    """
    Register a new administrator.
    """

    # Validate admin registration key
    if admin.admin_key != ADMIN_REGISTRATION_KEY:
        raise PermissionDeniedException()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            hashed_password,
            role
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            admin.username,
            admin.email,
            hash_password(admin.password),
            "admin",
        ),
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return UserResponse(
        id=user_id,
        username=admin.username,
        email=admin.email,
        role="admin",
        is_active=True,
    )

# --------------------------------------------------------
# update the users 
# --------------------------------------------------------

def update_current_user(
    current_user: UserResponse,
    user: UserUpdate,
) -> UserResponse:
    """
    Update the profile of the currently authenticated user.
    """

    # Create database connection
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # --------------------------------------------------
    # Update current user
    # --------------------------------------------------
    cursor.execute(
        """
        UPDATE users
        SET
            username = ?,
            email = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            user.username,
            user.email,
            current_user.id,
        ),
    )

    conn.commit()

    conn.close()

    # --------------------------------------------------
    # Return updated user
    # --------------------------------------------------
    return UserResponse(
        id=current_user.id,
        username=user.username,
        email=user.email,
        role=current_user.role,
        is_active=current_user.is_active,
    )