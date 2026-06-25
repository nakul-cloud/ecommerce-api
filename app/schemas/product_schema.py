from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """
    Request schema for creating a new product.
    """
    name:str = Field(
    ...,
    min_length=3,
    max_length=100,
    description="Name of the product"
    )



    description:str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Product description"
    )

    category:str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Product category"
    )

    price:float = Field(
        ...,
        gt=0,
        description="Selling price of the product"
    )

    stock_quantity:int = Field(
        ...,
        ge=0,
        description="Available stock quantity"
    )

    cost_price:float = Field(
        ...,
        gt=0,
        description="Cost price of the product"
    )



class ProductUpdate(BaseModel):
    """
    Request schema for updating an existing product.
    """
    name:Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Name of the product"
    )

    description:Optional[str]=Field(
        None,
        min_length=10,
        max_length=1000,
        description="Product description"
    )

    category:Optional[str]=Field(
        None,
        min_length=3,
        max_length=100,
        description="Product category"
    )

    price:Optional[float]=Field(
        None,
        gt=0,
        description="Selling price of the product"
    )

    stock_quantity:Optional[int]=Field(
        None,
        ge=0,
        description="Available stock quantity"
    )

    cost_price:Optional[float]=Field(
        None,
        gt=0,
        description="Cost price of the product"
    )



class ProductResponse(BaseModel):
    """
    Public schema returned to API clients
    """
    id: int
    name: str
    description: str
    category: str
    price: float
    stock_quantity: int


    
    