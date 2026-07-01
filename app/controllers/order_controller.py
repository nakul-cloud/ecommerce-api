from fastapi.responses import JSONResponse

from app.constants.status_codes import HTTP_201_CREATED
from app.constants.messages import (
    ORDER_CREATED,
    ORDER_FETCHED,
    ORDERS_FETCHED,
    ORDER_STATUS_UPDATED,
    ORDER_CANCELLED,
    ORDER_CONFIRMED,
    ORDER_PROCESSING,
    ORDER_PACKED,
)

from app.schemas.order_schema import (
    OrderCreate,
    OrderCancelRequest,
    OrderStatusUpdate,
    OrderPackingUpdate,
    PackingChecklist,
)
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

        order_data = order_service.create_order(
            order,
            current_user,
        )

        return success_response(
            message=ORDER_CREATED,
            data=order_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def index(
        current_user: UserResponse,
        page: int,
        limit: int,
    ) -> JSONResponse:
        """
        Retrieve paginated orders.

        Admin:
            Returns all orders.

        Customer:
            Returns only their own orders.
        """

        orders = order_service.get_orders(
            current_user=current_user,
            page=page,
            limit=limit,
        )

        return success_response(
            message=ORDERS_FETCHED,
            data=orders,
        )

    @staticmethod
    def show(
        order_id: int,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Retrieve a single order.
        """

        order_data = order_service.get_order_by_id(
            order_id=order_id,
            current_user=current_user,
        )

        return success_response(
            message=ORDER_FETCHED,
            data=order_data,
        )

    @staticmethod
    def update_status(
        order_id: int,
        status_update: OrderStatusUpdate,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Update the status of an order.
        """
        order_data = order_service.update_order_status(
            order_id=order_id,
            status_update=status_update,
            current_user=current_user,
        )
        return success_response(
            message=ORDER_STATUS_UPDATED,
            data=order_data,
        )

    @staticmethod
    def cancel(
        order_id: int,
        cancel_request: OrderCancelRequest,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Cancel a customer's own Pending order.
        Restores stock on success.
        """
        order_data = order_service.cancel_order(
            order_id=order_id,
            cancel_request=cancel_request,
            current_user=current_user,
        )
        return success_response(
            message=ORDER_CANCELLED,
            data=order_data,
        )

    @staticmethod
    def confirm(
        order_id: int,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Admin confirms a Pending order.
        Records confirmed_by and confirmed_at audit fields.
        """
        order_data = order_service.confirm_order(
            order_id=order_id,
            current_user=current_user,
        )
        return success_response(
            message=ORDER_CONFIRMED,
            data=order_data,
        )

    @staticmethod
    def pack(
        order_id: int,
        packing_update: OrderPackingUpdate,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Warehouse starts packaging a Confirmed order.
        Transition: Confirmed → Processing
        Saves warehouse_notes.
        """
        order_data = order_service.pack_order(
            order_id=order_id,
            packing_update=packing_update,
            current_user=current_user,
        )
        return success_response(
            message=ORDER_PROCESSING,
            data=order_data,
        )

    @staticmethod
    def ready(
        order_id: int,
        checklist: PackingChecklist,
        current_user: UserResponse,
    ) -> JSONResponse:
        """
        Warehouse marks a Processing order as ready for shipment.
        Transition: Processing → Ready For Shipment
        Saves checklist fields and audit info.
        """
        order_data = order_service.ready_order(
            order_id=order_id,
            checklist=checklist,
            current_user=current_user,
        )
        return success_response(
            message=ORDER_PACKED,
            data=order_data,
        )