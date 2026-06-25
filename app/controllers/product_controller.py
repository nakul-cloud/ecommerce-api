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
    