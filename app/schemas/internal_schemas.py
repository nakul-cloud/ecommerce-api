from pydantic import BaseModel


class ValidatedOrderItem(BaseModel):
    """
    Internal model used after validating an order item.
    """

    product_id:int
    quantity:int
    unit_price:float

