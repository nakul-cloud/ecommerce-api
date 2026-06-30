from app.constants.roles import ADMIN, CUSTOMER
from app.auth.password import hash_password, verify_password
from app.config.database import get_db_connection
from app.config.settings import ADMIN_REGISTRATION_KEY
from app.exceptions.custom_exceptions import (
    InvalidPasswordException,
    PermissionDeniedException,
)
from app.schemas.user_schema import (
    AdminRegisterRequest,
    ChangePasswordRequest,
    UserCreate,
    UserResponse,
    UserUpdate,
)


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
        role=CUSTOMER,
        is_active=True,
    )


def create_admin(admin: AdminRegisterRequest) -> UserResponse:
    """
    Register a new administrator.
    """
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
            ADMIN,
        ),
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return UserResponse(
        id=user_id,
        username=admin.username,
        email=admin.email,
        role=ADMIN,
        is_active=True,
    )


def update_current_user(
    current_user: UserResponse,
    user: UserUpdate,
) -> UserResponse:
    """
    Update the profile of the currently authenticated user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

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
) -> None:
    """
    Change the password of the currently authenticated user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

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

    if not verify_password(
        password_data.old_password,
        user["hashed_password"],
    ):
        conn.close()
        raise InvalidPasswordException()

    new_password = hash_password(password_data.new_password)

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
