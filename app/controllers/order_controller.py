from app.config.database import get_db_connection

from app.schemas.order_schema import (
    OrderCreate,
    OrderItem,
    OrderResponse,
)

from app.schemas.internal_schemas import ValidatedOrderItem

from app.exceptions.custom_exceptions import (
    ProductNotFoundException,
    ProductOutOfStockException,
    OrderNotFoundException
)


def create_order(order: OrderCreate) -> OrderResponse:
    """
    Create a new customer order.
    """

    # Create database connection
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # Store total order amount
    total_amount = 0.0

    # Store validated products
    validated_products: list[ValidatedOrderItem] = []

    # -------------------------------------------------
    # Validate products and calculate total amount
    # -------------------------------------------------
    for item in order.items:

        # Fetch product from database
        cursor.execute(
            """
            SELECT
                id,
                price,
                stock_quantity
            FROM products
            WHERE id = ?
            """,
            (item.product_id,),
        )

        product = cursor.fetchone()

        # Product does not exist
        if product is None:
            conn.close()
            raise ProductNotFoundException(item.product_id)

        # Check stock availability
        if product["stock_quantity"] < item.quantity:
            conn.close()
            raise ProductOutOfStockException(item.product_id)

        # Calculate running total
        total_amount += product["price"] * item.quantity

        # Store validated product
        validated_products.append(
            ValidatedOrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product["price"],
            )
        )

    # -------------------------------------------------
    # Create order
    # -------------------------------------------------
    cursor.execute(
        """
        INSERT INTO orders
        (
            total_amount
        )
        VALUES (?)
        """,
        (total_amount,),
    )

    # Get newly created order ID
    order_id = cursor.lastrowid

    # -------------------------------------------------
    # Insert order items and update stock
    # -------------------------------------------------
    for product in validated_products:

        # Insert order item
        cursor.execute(
            """
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                order_id,
                product.product_id,
                product.quantity,
                product.unit_price,
            ),
        )

        # Update product stock
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity - ?
            WHERE id = ?
            """,
            (
                product.quantity,
                product.product_id,
            ),
        )

    # -------------------------------------------------
    # Commit transaction
    # -------------------------------------------------
    conn.commit()

    # Close connection
    conn.close()

    # -------------------------------------------------
    # Return response
    # -------------------------------------------------
    return OrderResponse(
        id=order_id,
        total_amount=total_amount,
        items=order.items,
    )

   # -------------------------------------------------
   # Get all orders
   # -------------------------------------------------
   
def get_all_orders() -> list[OrderResponse]:
    """
    Retrieve all orders from the database.
    """

    # Create database connection
    conn = get_db_connection()

    # Create cursor
    cursor = conn.cursor()

    # Fetch all orders
    cursor.execute(
        """
        SELECT
            id,
            total_amount
        FROM orders
        ORDER BY id
        """
    )

    # Fetch all rows
    orders = cursor.fetchall()

    # Store API responses
    order_responses = []

    for order in orders:

        # Fetch all items belonging to this order
        cursor.execute(
            """
            SELECT
                product_id,
                quantity
            FROM order_items
            WHERE order_id = ?
            """,
            (order["id"],),
        )

        item_rows = cursor.fetchall()

        # Convert database rows into OrderItem objects
        items = [
            OrderItem(
                product_id=item["product_id"],
                quantity=item["quantity"]
            )
            for item in item_rows
        ]

        # Add to response list
        order_responses.append(
            OrderResponse(
                id=order["id"],
                total_amount=order["total_amount"],
                items=items,
            )
        )

    # Close connection
    conn.close()

    return order_responses

#-------------------------------------------------------------
# Get Order by ID
#-------------------------------------------------------------

def get_order_by_id(order_id:int)-> OrderResponse:
    """
    Retrieve a single order by its ID.
    """

    conn = get_db_connection()
    
    cursor = conn.cursor()

    # ---------------------------------------------
    # Fetch the requested order
    # ---------------------------------------------
    cursor.execute(
        """
        SELECT
            id,
            total_amount
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )

    order = cursor.fetchone()

    # Order does not exist
    if order is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # ---------------------------------------------
    # Fetch all items belonging to this order
    # ---------------------------------------------
    cursor.execute(
        """
        SELECT
            product_id,
            quantity
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,),
    )

    item_rows = cursor.fetchall()

    # Convert database rows into OrderItem objects
    items = [
        OrderItem(
            product_id=item["product_id"],
            quantity=item["quantity"],
        )
        for item in item_rows
    ]

    # Close connection
    conn.close()

    # Return API response
    return OrderResponse(
        id=order["id"],
        total_amount=order["total_amount"],
        items=items,
    )