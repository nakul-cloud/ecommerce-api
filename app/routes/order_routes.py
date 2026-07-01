from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from app.auth.dependencies import (
    get_current_user,
    require_role,
)
from app.constants.roles import ADMIN, WAREHOUSE

from app.controllers.order_controller import OrderController

from app.schemas.order_schema import (
    OrderCreate,
    OrderCancelRequest,
    StandardOrderResponse,
    StandardOrderListResponse,
    OrderStatusUpdate,
    OrderPackingUpdate,
    PackingChecklist,
)

from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# --------------------------------------------------
# Create Order (Authenticated User)
# --------------------------------------------------

@router.post(
    "",
    response_model=StandardOrderResponse,
    status_code=201,
)
def store(
    order: OrderCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Create a new order for the currently authenticated user.
    """

    return OrderController.store(
        order=order,
        current_user=current_user,
    )


# --------------------------------------------------
# Get Orders (Paginated)
# --------------------------------------------------

@router.get(
    "",
    response_model=StandardOrderListResponse,
)
def index(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of records per page",
    ),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve paginated orders.

    Admin:
        Can view all orders.

    Customer:
        Can view only their own orders.
    """

    return OrderController.index(
        current_user=current_user,
        page=page,
        limit=limit,
    )


# --------------------------------------------------
# Get Order By ID
# --------------------------------------------------

@router.get(
    "/{order_id}",
    response_model=StandardOrderResponse,
)
def show(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve a single order by its ID.

    Admin:
        Can view any order.

    Customer:
        Can view only their own order.
    """

    return OrderController.show(
        order_id=order_id,
        current_user=current_user,
    )


# --------------------------------------------------
# Update Order Status (Admin Only)
# --------------------------------------------------
@router.patch(
    "/{order_id}/status",
    response_model=StandardOrderResponse,
)
def update_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Update the status of an order.

    Admin only.
    """
    return OrderController.update_status(
        order_id=order_id,
        status_update=status_update,
        current_user=current_user,
    )


# --------------------------------------------------
# Cancel Order (Customer — own Pending orders only)
# --------------------------------------------------
@router.patch(
    "/{order_id}/cancel",
    response_model=StandardOrderResponse,
)
def cancel(
    order_id: int,
    cancel_request: OrderCancelRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Cancel a Pending order.

    Customer:
        Can only cancel their own orders while status is Pending.
        Stock is restored on cancellation.
    """
    return OrderController.cancel(
        order_id=order_id,
        cancel_request=cancel_request,
        current_user=current_user,
    )


# --------------------------------------------------
# Confirm Order (Admin only)
# --------------------------------------------------
@router.patch(
    "/{order_id}/confirm",
    response_model=StandardOrderResponse,
)
def confirm(
    order_id: int,
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Confirm a Pending order.

    Admin only.
    Transitions order from Pending to Confirmed.
    Records confirmed_by and confirmed_at.
    """
    return OrderController.confirm(
        order_id=order_id,
        current_user=current_user,
    )


# --------------------------------------------------
# Pack Order (Warehouse only)
# --------------------------------------------------
@router.patch(
    "/{order_id}/pack",
    response_model=StandardOrderResponse,
)
def pack(
    order_id: int,
    packing_update: OrderPackingUpdate,
    current_user: UserResponse = Depends(require_role(WAREHOUSE)),
):
    """
    Start packaging a Confirmed order.

    Warehouse only.
    Transitions order from Confirmed to Processing.
    Saves warehouse_notes.
    """
    return OrderController.pack(
        order_id=order_id,
        packing_update=packing_update,
        current_user=current_user,
    )


# --------------------------------------------------
# Ready Order (Warehouse only)
# --------------------------------------------------
@router.patch(
    "/{order_id}/ready",
    response_model=StandardOrderResponse,
)
def ready(
    order_id: int,
    checklist: PackingChecklist,
    current_user: UserResponse = Depends(require_role(WAREHOUSE)),
):
    """
    Mark a Processing order as ready for shipment.

    Warehouse only.
    Transitions order from Processing to Ready For Shipment.
    Saves checklist and audit details.
    """
    return OrderController.ready(
        order_id=order_id,
        checklist=checklist,
        current_user=current_user,
    )