from app.config.database import get_db_connection
from app.config.settings import ADMIN_REGISTRATION_KEY

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    AdminRegisterRequest,
    ChangePasswordRequest,
)

from app.auth.password import (
    hash_password,
    verify_password,
)

from app.exceptions.custom_exceptions import (
    PermissionDeniedException,
    InvalidPasswordException
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

def change_password(
    current_user: UserResponse,
    password_data: ChangePasswordRequest,
) -> dict:
    """
    Change the password of the currently authenticated user.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # ----------------------------------------
    # Fetch current hashed password
    # ----------------------------------------

    cursor.execute(
        """
        SELECT hashed_password
        FROM users
        WHERE id = ?
        """,
        (current_user.id,),
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        raise PermissionDeniedException()

    # ----------------------------------------
    # Verify old password
    # ----------------------------------------

    if not verify_password(
        password_data.old_password,
        user["hashed_password"],
    ):
        conn.close()
        raise InvalidPasswordException()

    # ----------------------------------------
    # Hash new password
    # ----------------------------------------

    new_password = hash_password(
        password_data.new_password,
    )

    # ----------------------------------------
    # Update password
    # ----------------------------------------

    cursor.execute(
        """
        UPDATE users
        SET
            hashed_password = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            new_password,
            current_user.id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "message": "Password changed successfully."
    }