from typing import List

from app.config.database import get_db_connection
from app.exceptions.custom_exceptions import ProductNotFoundException
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


def create_product(product: ProductCreate) -> ProductResponse:
    """
    Create a new product in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO products
        (
            name,
            description,
            category,
            price,
            stock_quantity,
            cost_price
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            product.name,
            product.description,
            product.category,
            product.price,
            product.stock_quantity,
            product.cost_price,
        ),
    )

    conn.commit()
    product_id = cursor.lastrowid
    conn.close()

    return ProductResponse(
        id=product_id,
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price,
        stock_quantity=product.stock_quantity,
    )


def get_all_products() -> List[ProductResponse]:
    """
    Retrieve all products from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            description,
            category,
            price,
            stock_quantity
        FROM products
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        ProductResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            category=row["category"],
            price=row["price"],
            stock_quantity=row["stock_quantity"],
        )
        for row in rows
    ]


def get_product_by_id(product_id: int) -> ProductResponse:
    """
    Retrieve a single product by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            description,
            category,
            price,
            stock_quantity
        FROM products
        WHERE id = ?
        """,
        (product_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise ProductNotFoundException(product_id)

    return ProductResponse(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        category=row["category"],
        price=row["price"],
        stock_quantity=row["stock_quantity"],
    )


def delete_product(product_id: int) -> None:
    """
    Delete a product by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise ProductNotFoundException(product_id)

    conn.close()


def update_product(
    product_id: int,
    product: ProductUpdate,
) -> ProductResponse:
    """
    Update an existing product.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = ?
        """,
        (product_id,),
    )

    existing_product = cursor.fetchone()

    if existing_product is None:
        conn.close()
        raise ProductNotFoundException(product_id)

    updated_name = product.name if product.name is not None else existing_product["name"]
    updated_description = (
        product.description
        if product.description is not None
        else existing_product["description"]
    )
    updated_category = (
        product.category if product.category is not None else existing_product["category"]
    )
    updated_price = product.price if product.price is not None else existing_product["price"]
    updated_stock = (
        product.stock_quantity
        if product.stock_quantity is not None
        else existing_product["stock_quantity"]
    )
    updated_cost_price = (
        product.cost_price
        if product.cost_price is not None
        else existing_product["cost_price"]
    )

    cursor.execute(
        """
        UPDATE products
        SET
            name = ?,
            description = ?,
            category = ?,
            price = ?,
            stock_quantity = ?,
            cost_price = ?
        WHERE id = ?
        """,
        (
            updated_name,
            updated_description,
            updated_category,
            updated_price,
            updated_stock,
            updated_cost_price,
            product_id,
        ),
    )

    conn.commit()
    conn.close()

    return ProductResponse(
        id=product_id,
        name=updated_name,
        description=updated_description,
        category=updated_category,
        price=updated_price,
        stock_quantity=updated_stock,
    )
