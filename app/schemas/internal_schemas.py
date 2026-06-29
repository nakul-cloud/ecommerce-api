from pydantic import BaseModel


class ValidatedOrderItem(BaseModel):
    """
    Internal model used after validating an order item.
    This model is never exposed to the client.
    """

    product_id: int

    product_name: str

    quantity: int

    unit_price: float

    subtotal: float