from fastapi.responses import JSONResponse

from app.constants.status_codes import HTTP_201_CREATED
from app.constants.messages import (
    ADMIN_REGISTERED,
    PASSWORD_CHANGED,
    PROFILE_FETCHED,
    PROFILE_UPDATED,
    USER_REGISTERED,
    WAREHOUSE_REGISTERED,
)
from app.schemas.user_schema import (
    AdminRegisterRequest,
    ChangePasswordRequest,
    UserCreate,
    UserResponse,
    UserUpdate,
    WarehouseRegisterRequest,
)
from app.services import user_service
from app.utils.response import success_response


class UserController:
    @staticmethod
    def store(user: UserCreate) -> JSONResponse:
        """
        Register a new customer.
        """
        user_data = user_service.create_user(user)
        return success_response(
            message=USER_REGISTERED,
            data=user_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def store_admin(admin: AdminRegisterRequest) -> JSONResponse:
        """
        Register a new administrator.
        """
        user_data = user_service.create_admin(admin)
        return success_response(
            message=ADMIN_REGISTERED,
            data=user_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def store_warehouse(warehouse: WarehouseRegisterRequest) -> JSONResponse:
        """
        Register a new warehouse staff member. Admin only.
        """
        user_data = user_service.create_warehouse_user(warehouse)
        return success_response(
            message=WAREHOUSE_REGISTERED,
            data=user_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def show(current_user: UserResponse) -> JSONResponse:
        """
        Return the current authenticated user's profile.
        """
        return success_response(
            message=PROFILE_FETCHED,
            data=current_user,
        )

    @staticmethod
    def update(
        current_user: UserResponse,
        user: UserUpdate,
    ) -> JSONResponse:
        """
        Update the profile of the currently authenticated user.
        """
        user_data = user_service.update_current_user(current_user, user)
        return success_response(
            message=PROFILE_UPDATED,
            data=user_data,
        )

    @staticmethod
    def change_password(
        current_user: UserResponse,
        password_data: ChangePasswordRequest,
    ) -> JSONResponse:
        """
        Change the password of the currently authenticated user.
        """
        user_service.change_password(current_user, password_data)
        return success_response(message=PASSWORD_CHANGED)
