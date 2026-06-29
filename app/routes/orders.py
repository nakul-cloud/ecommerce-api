from typing import List

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import (
    get_current_user,
    require_role,
)

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
# Create Order (Authenticated User)
# --------------------------------------------------

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_order(
    order: OrderCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Create a new order for the currently authenticated user.
    """
    return create_order(
        order=order,
        current_user=current_user,
    )


# --------------------------------------------------
# Get All Orders (Admin Only)
# --------------------------------------------------

@router.get(
    "",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def get_orders(
    current_user: UserResponse = Depends(
        require_role("admin")
    ),
):
    """
    Retrieve all orders.
    Admin only.
    """
    return get_all_orders()


# --------------------------------------------------
# Get Order By ID
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
    """
    return get_order_by_id(order_id)