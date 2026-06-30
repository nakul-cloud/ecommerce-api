from fastapi.responses import JSONResponse

from app.constants.status_codes import HTTP_201_CREATED
from app.constants.messages import (
    PRODUCT_CREATED,
    PRODUCT_DELETED,
    PRODUCT_FETCHED,
    PRODUCT_UPDATED,
    PRODUCTS_FETCHED,
)
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services import product_service
from app.utils.response import success_response


class ProductController:
    @staticmethod
    def store(product: ProductCreate) -> JSONResponse:
        """
        Create a new product.
        """
        product_data = product_service.create_product(product)
        return success_response(
            message=PRODUCT_CREATED,
            data=product_data,
            status_code=HTTP_201_CREATED,
        )

    @staticmethod
    def index() -> JSONResponse:
        """
        Retrieve all products.
        """
        products = product_service.get_all_products()
        return success_response(
            message=PRODUCTS_FETCHED,
            data=products,
        )

    @staticmethod
    def show(product_id: int) -> JSONResponse:
        """
        Retrieve a single product by its ID.
        """
        product_data = product_service.get_product_by_id(product_id)
        return success_response(
            message=PRODUCT_FETCHED,
            data=product_data,
        )

    @staticmethod
    def destroy(product_id: int) -> JSONResponse:
        """
        Delete a product by its ID.
        """
        product_service.delete_product(product_id)
        return success_response(message=PRODUCT_DELETED)

    @staticmethod
    def update(
        product_id: int,
        product: ProductUpdate,
    ) -> JSONResponse:
        """
        Update an existing product.
        """
        product_data = product_service.update_product(product_id, product)
        return success_response(
            message=PRODUCT_UPDATED,
            data=product_data,
        )
