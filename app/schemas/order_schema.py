from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# ==================================================
# Order Item Create
# ==================================================

class OrderItemCreate(BaseModel):
    """
    Represents a single product in an order.
    """

    product_id: int = Field(
        ...,
        gt=0,
        description="Unique ID of the product.",
        example=1,
    )

    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity of the product to order.",
        example=2,
    )


# ==================================================
# Order Create
# ==================================================

class OrderCreate(BaseModel):
    """
    Request schema for creating a new order.
    """

    items: List[OrderItemCreate] = Field(
        ...,
        min_length=1,
        description="List of products included in the order.",
        example=[
            {
                "product_id": 1,
                "quantity": 2,
            },
            {
                "product_id": 5,
                "quantity": 1,
            },
        ],
    )


# ==================================================
# Order Item Response
# ==================================================

class OrderItemResponse(BaseModel):
    """
    Represents a single product returned in an order.
    """

    product_id: int = Field(
        ...,
        description="Product ID.",
    )

    product_name: str = Field(
        ...,
        description="Name of the product.",
    )

    quantity: int = Field(
        ...,
        description="Quantity ordered.",
    )

    unit_price: float = Field(
        ...,
        description="Price per unit at the time of purchase.",
    )

    subtotal: float = Field(
        ...,
        description="Subtotal for this order item.",
    )


# ==================================================
# Order Response
# ==================================================

class OrderResponse(BaseModel):
    """
    Public schema returned after an order is created or retrieved.
    """

    id: int = Field(
        ...,
        description="Unique order ID.",
    )

    status: str = Field(
        ...,
        description="Current status of the order.",
        example="Pending",
    )

    total_amount: float = Field(
        ...,
        description="Total amount of the order.",
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the order was created.",
    )

    items: List[OrderItemResponse] = Field(
        ...,
        description="List of products included in the order.",
    )


# ==================================================
# Standard API Response Wrappers
# ==================================================

class StandardOrderResponse(BaseModel):
    status: str = Field("success", example="success")
    message: str = Field(..., example="Order action succeeded")
    data: OrderResponse


class StandardOrderListResponse(BaseModel):
    status: str = Field("success", example="success")
    message: str = Field(..., example="Orders fetched successfully")
    data: List[OrderResponse]
