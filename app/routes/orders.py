from app.config import dependencies
from fastapi import APIRouter, Depends, status

from app.config.dependencies import verify_admin_api_key

from app.controllers.order_controller import(
    create_order,
    get_all_orders,
    get_order_by_id,
)

from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
)

router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_admin_api_key)],
    summary="create a new order"
)
def create_new_order(order:OrderCreate):
    """
    Create a new customer order
    """
    return create_order(order)


@router.get(
    "",
    response_model=list[OrderResponse],
)
def get_orders():
    """
    Retrieve all orders.
    """
    return get_all_orders()

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(order_id:int):
    """
    Retrieve a single order by its ID.
    """
    return get_order_by_id(order_id)