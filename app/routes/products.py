from typing import List

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import (
    get_current_user,
    require_role,
)

from app.controllers.product_controller import (
    create_product,
    get_all_products,
    get_product_by_id,
    delete_product,
)

from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
)

from app.schemas.user_schema import UserResponse


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# --------------------------------------------------
# Create Product (Admin Only)
# --------------------------------------------------
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_product(
    product: ProductCreate,
    current_user: UserResponse = Depends(
        require_role("admin")
    ),
):
    """
    Create a new product.
    Admin only.
    """
    return create_product(product)


# --------------------------------------------------
# Get All Products (Public)
# --------------------------------------------------
@router.get(
    "",
    response_model=List[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def get_products() -> List[ProductResponse]:
    """
    Retrieve all products.
    """
    return get_all_products()


# --------------------------------------------------
# Get Product By ID (Public)
# --------------------------------------------------
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def get_product(
    product_id: int,
) -> ProductResponse:
    """
    Retrieve a single product by its ID.
    """
    return get_product_by_id(product_id)


# --------------------------------------------------
# Delete Product (Admin Only)
# --------------------------------------------------
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
)
def delete_existing_product(
    product_id: int,
    current_user: UserResponse = Depends(
        require_role("admin")
    ),
):
    """
    Delete a product by its ID.
    Admin only.
    """
    return delete_product(product_id)