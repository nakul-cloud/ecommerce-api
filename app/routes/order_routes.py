from app.constants.roles import ADMIN
from fastapi import APIRouter, Depends

from app.auth.dependencies import (
    get_current_user,
    require_role,
)
from app.controllers.order_controller import OrderController
from app.schemas.order_schema import OrderCreate
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# --------------------------------------------------
# Create Order (Authenticated User)
# --------------------------------------------------
@router.post("")
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
# Get All Orders (Admin Only)
# --------------------------------------------------
@router.get("")
def index(
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Retrieve all orders.
    Admin only.
    """
    return OrderController.index()


# --------------------------------------------------
# Get Order By ID
# --------------------------------------------------
@router.get("/{order_id}")
def show(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve a single order by its ID.

    Admin:
        Can view any order
    
    Customer:
        Can view only their order
    """

    return OrderController.show(
        order_id=order_id,
        current_user=current_user,
        )
