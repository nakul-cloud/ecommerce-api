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
# Order Status Update
# ==================================================

class OrderStatusUpdate(BaseModel):
    """
    Request schema for updating an order status.
    """

    status: str = Field(
        ...,
        description="New status of the order.",
        example="Shipped",
    )



# ==================================================
# Order Cancel Request
# ==================================================

class OrderCancelRequest(BaseModel):
    """
    Request schema for cancelling an order.
    Reason is optional — customer does not have to explain.
    """

    reason: str | None = Field(
        None,
        description="Optional reason for cancellation.",
        example="Changed my mind.",
    )


# ==================================================
# Order Packing Update (Warehouse)
# ==================================================

class OrderPackingUpdate(BaseModel):
    """
    Request schema for warehouse starting packaging.
    """
    warehouse_notes: str | None = Field(
        None,
        description="Notes from warehouse regarding picking/packing.",
        example="Fragile item, pack with extra bubble wrap.",
    )


# ==================================================
# Packing Checklist (Warehouse)
# ==================================================

class PackingChecklist(BaseModel):
    """
    Checklist submitted when order is packed and ready.
    """
    all_items_verified: bool = Field(
        ...,
        description="Whether all items in the order have been verified.",
        example=True,
    )
    package_weight: float = Field(
        ...,
        gt=0.0,
        description="Total package weight in kilograms.",
        example=2.4,
    )
    package_dimensions: str = Field(
        ...,
        description="Dimensions of the package (e.g. LxWxH cm).",
        example="20x15x10 cm",
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

    user_id: int | None = Field(
        None,
        description="ID of the user who placed the order.",
    )

    username: str | None = Field(
        None,
        description="Username of the user who placed the order.",
    )

    warehouse_notes: str | None = Field(
        None,
        description="Fulfillment notes from warehouse.",
    )

    all_items_verified: bool | None = Field(
        None,
        description="Whether order items are verified.",
    )

    package_weight: float | None = Field(
        None,
        description="Package weight.",
    )

    package_dimensions: str | None = Field(
        None,
        description="Package dimensions.",
    )



# ==================================================
# Pagination Response
# ==================================================

class PaginationResponse(BaseModel):
    """
    Pagination metadata.
    """

    page: int = Field(
        ...,
        description="Current page number.",
        example=1,
    )

    limit: int = Field(
        ...,
        description="Maximum records per page.",
        example=10,
    )

    total_records: int = Field(
        ...,
        description="Total number of matching records.",
        example=250,
    )

    total_pages: int = Field(
        ...,
        description="Total available pages.",
        example=25,
    )


# ==================================================
# Paginated Orders Response
# ==================================================

class PaginatedOrdersResponse(BaseModel):
    """
    Paginated list of orders.
    """

    pagination: PaginationResponse

    orders: List[OrderResponse]


# ==================================================
# Standard API Response Wrappers
# ==================================================

class StandardOrderResponse(BaseModel):
    """
    Standard response for a single order.
    """

    status: str = Field(
        "success",
        example="success",
    )

    message: str = Field(
        ...,
        example="Order created successfully.",
    )

    data: OrderResponse


class StandardOrderListResponse(BaseModel):
    """
    Standard response for paginated orders.
    """

    status: str = Field(
        "success",
        example="success",
    )

    message: str = Field(
        ...,
        example="Orders fetched successfully.",
    )

    data: PaginatedOrdersResponse