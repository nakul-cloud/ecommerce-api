from fastapi import APIRouter,status
from app.controllers.product_controller import create_product
from app.schemas.product_schema import ProductCreate,ProductResponse


router = APIRouter(
    prefix='/products',
    tags=['Products'],
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_new_product(product:ProductCreate):
    """
    Create a new product
    """
    return create_product(product)