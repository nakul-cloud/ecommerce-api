from app.constants.roles import ADMIN
from fastapi import APIRouter, Depends

from app.auth.dependencies import require_role
from app.controllers.product_controller import ProductController
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
)
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# --------------------------------------------------
# Create Product (Admin Only)
# --------------------------------------------------
@router.post("")
def store(
    product: ProductCreate,
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Create a new product.
    Admin only.
    """
    return ProductController.store(product)


# --------------------------------------------------
# Get All Products (Public)
# --------------------------------------------------
@router.get("")
def index():
    """
    Retrieve all products.
    """
    return ProductController.index()


# --------------------------------------------------
# Get Product By ID (Public)
# --------------------------------------------------
@router.get("/{product_id}")
def show(
    product_id: int,
):
    """
    Retrieve a single product by its ID.
    """
    return ProductController.show(product_id)


# --------------------------------------------------
# Update Product (Admin Only)
# --------------------------------------------------
@router.put(
    "/{product_id}",
    summary="Update an existing product",
)
def update(
    product_id: int,
    product: ProductUpdate,
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Update an existing product.
    Admin only.
    """
    return ProductController.update(
        product_id=product_id,
        product=product,
    )


# --------------------------------------------------
# Delete Product (Admin Only)
# --------------------------------------------------
@router.delete("/{product_id}")
def destroy(
    product_id: int,
    current_user: UserResponse = Depends(require_role(ADMIN)),
):
    """
    Delete a product by its ID.
    Admin only.
    """
    return ProductController.destroy(product_id)
