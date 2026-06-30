from fastapi.responses import JSONResponse

from app.constants.status_codes import HTTP_201_CREATED
from app.constants.messages import (
    ORDER_CREATED,
    ORDER_FETCHED,
    ORDERS_FETCHED,
)
from app.schemas.order_schema import OrderCreate
from app.schemas.user_schema import UserResponse
from app.services import order_service
from app.utils.response import success_response


class OrderController:
    @staticmethod
    def store(
        order: OrderCreate,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Create a new order for the currently authenticated user.
        """
        order_data = order_service.create_order(order, current_user)
        return success_response(
            message=ORDER_CREATED,
            data=order_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def index() -> JSONResponse:
        """
        Get all orders.
        """
        orders = order_service.get_all_orders()
        return success_response(
            message=ORDERS_FETCHED,
            data=orders,
        )

    @staticmethod
    def show(order_id: int) -> JSONResponse:
        """
        Get order by ID.
        """
        order_data = order_service.get_order_by_id(order_id)
        return success_response(
            message=ORDER_FETCHED,
            data=order_data,
        )
