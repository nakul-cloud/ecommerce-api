from typing import List
from pydantic import BaseModel,Field


class OrderItem(BaseModel):
    """
    Represents a single product in an order
    """
    product_id:int=Field(
        ...,
        gt=0,
        description="ID of the product"
    )

    quantity:int=Field(
        ...,
        gt=0,
        description="Quantity of the product"
    )
'''
Because an order contains multiple order items, we use a nested List[OrderItem]
 so FastAPI validates the entire order request and every order item inside it.
'''

class OrderCreate(BaseModel):
    """
    Request schema for creating a new order
    """
    items:List[OrderItem]=Field(
        ...,
        min_length=1,
        description="List of products included in the order"
    )


class OrderResponse(BaseModel):
    """
    Public schema returned after an order is created or retrieved
    """
    id:int
    total_amount:float
    items:List[OrderItem]