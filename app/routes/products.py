from app.controllers.product_controller import delete_product
from typing import List 
from fastapi import APIRouter,status
from app.controllers.product_controller import (
    create_product,
    get_all_products,
    get_product_by_id,
)
from app.schemas.product_schema import ProductCreate,ProductResponse
from fastapi import Depends
from app.config.dependencies import verify_admin_api_key

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_admin_api_key)],
)

def create_new_product(product:ProductCreate):
    """
    Create a new product
    """
    return create_product(product)

@router.get(
    "",
    response_model=List[ProductResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_admin_api_key)],
)
def get_products()-> List[ProductResponse]:
    """
    Retrieve all products
    """
    return get_all_products()

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def get_product(product_id: int) -> ProductResponse:
    """
    Retrieve a single product by its ID.
    """
    return get_product_by_id(product_id)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
)
def del_product(product_id:int)-> dict:
    """
    Delete a product by its ID
    """
    return delete_product(product_id)