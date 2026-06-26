from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user

from app.controllers.order_controller import (
    create_order,
    get_all_orders,
    get_order_by_id,
)

from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
)

from app.schemas.user_schema import UserResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# --------------------------------------------------
# Create Order (Authenticated Users)
# --------------------------------------------------
@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
def create_new_order(
    order: OrderCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Create a new customer order.
    Requires authentication.
    """
    return create_order(order)


# --------------------------------------------------
# Get All Orders (Authenticated Users)
# --------------------------------------------------
@router.get(
    "",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def get_orders(
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve all orders.
    Requires authentication.
    """
    return get_all_orders()


# --------------------------------------------------
# Get Order By ID (Authenticated Users)
# --------------------------------------------------
@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve a single order by its ID.
    Requires authentication.
    """
    return get_order_by_id(order_id)