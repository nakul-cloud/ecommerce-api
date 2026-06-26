from app.config.database import get_db_connection
from app.config.settings import ADMIN_REGISTRATION_KEY

from app.schemas.user_schema import (
    UserCreate,
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