from multiprocessing.sharedctypes import Value
from check_db import cursor
from typing import List
from app.config.database import get_db_connection
from app.schemas.product_schema import(
    ProductCreate,
    ProductUpdate,
    ProductResponse
)


def create_product(product:ProductCreate) -> ProductResponse:
    """
    Create a new product in the database.
    """
    # Create database connection
    conn = get_db_connection()

    # Create cursor
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
        VALUES (?,?,?,?,?,?)
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

    # Save changes
    conn.commit()

    # Get newly created product ID
    product_id = cursor.lastrowid

    # Close connection
    conn.close()
    

    # Return the API response
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

    # Create database connectionNEX
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # Fetch all products
    cursor.execute("""
        SELECT
            id,
            name,
            description,
            category,
            price,
            stock_quantity
        FROM products
    """)
    # Fetch all rows
    rows = cursor.fetchall()

    # Close connection
    conn.close()

    # Convert database rows into ProductResponse objects
    products = [
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

    return products

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
        raise ValueError("Product not found")

    return ProductResponse(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        category=row["category"],
        price=row["price"],
        stock_quantity=row["stock_quantity"],
    )

    
def delete_product(product_id:int) -> dict:
    """
    Delete a product by its ID
    """
    conn=get_db_connection()
    cursor=conn.cursor()

# Delete the product
    cursor.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,),
    )

    conn.commit()

    # check whether row was delected 

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Product not found")

    conn.close()

    return{
        "message": "Product delected successfully"
    }
    