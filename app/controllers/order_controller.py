from datetime import datetime

from app.config.database import get_db_connection

from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderItemResponse,
)

from app.schemas.user_schema import UserResponse

from app.schemas.internal_schemas import (
    ValidatedOrderItem,
)

from app.exceptions.custom_exceptions import (
    ProductNotFoundException,
    ProductOutOfStockException,
    OrderNotFoundException,
)


def create_order(
    order: OrderCreate,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Create a new order for the currently authenticated user.

    Workflow:
    1. Validate every requested product.
    2. Check product stock.
    3. Calculate subtotal and total amount.
    4. Create the order.
    5. Insert order items.
    6. Reduce product inventory.
    7. Commit transaction.
    8. Return the complete order response.
    """

    # -------------------------------------------------
    # Create database connection
    # -------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()

    # Running total for the order
    total_amount = 0.0

    # Store validated products before inserting
    validated_products: list[ValidatedOrderItem] = []

    try:

        # -------------------------------------------------
        # Validate every product in the request
        # -------------------------------------------------
        for item in order.items:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
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
                raise ProductNotFoundException(item.product_id)

            # Product does not have enough stock
            if product["stock_quantity"] < item.quantity:
                raise ProductOutOfStockException(item.product_id)

            # Calculate subtotal
            subtotal = round(
                product["price"] * item.quantity,
                2,
            )

            # Add to running total
            total_amount = round(
                total_amount + subtotal,
                2,
            )

            # Store validated product for later use
            validated_products.append(
                ValidatedOrderItem(
                    product_id=product["id"],
                    product_name=product["name"],
                    quantity=item.quantity,
                    unit_price=product["price"],
                    subtotal=subtotal,
                )
            )

        # -------------------------------------------------
        # Create order
        # -------------------------------------------------
        cursor.execute(
            """
            INSERT INTO orders
            (
                user_id,
                status,
                total_amount
            )
            VALUES (?, ?, ?)
            """,
            (
                current_user.id,
                "Pending",
                total_amount,
            ),
        )

        # Newly created order ID
        order_id = cursor.lastrowid

        # -------------------------------------------------
        # Insert every order item
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

            # -------------------------------------------------
            # Reduce stock safely
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - ?
                WHERE id = ?
                AND stock_quantity >= ?
                """,
                (
                    product.quantity,
                    product.product_id,
                    product.quantity,
                ),
            )

            # Make sure the update actually happened
            if cursor.rowcount == 0:
                raise ProductOutOfStockException(
                    product.product_id
                )
        # -------------------------------------------------
        # Save all changes
        # -------------------------------------------------
        conn.commit()

        # -------------------------------------------------
        # Fetch order metadata
        # -------------------------------------------------
        cursor.execute(
            """
            SELECT
                created_at,
                status
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        )

        created_order = cursor.fetchone()

        # -------------------------------------------------
        # Convert validated items into response objects
        # -------------------------------------------------
        response_items = []

        for product in validated_products:

            response_items.append(
                OrderItemResponse(
                    product_id=product.product_id,
                    product_name=product.product_name,
                    quantity=product.quantity,
                    unit_price=product.unit_price,
                    subtotal=product.subtotal,
                )
            )

        # -------------------------------------------------
        # Return API response
        # -------------------------------------------------
        return OrderResponse(
            id=order_id,
            status=created_order["status"],
            total_amount=total_amount,
            created_at=datetime.fromisoformat(
                created_order["created_at"]
            ),
            items=response_items,
        )

    # -------------------------------------------------
    # Rollback transaction if any error occurs
    # -------------------------------------------------
    except Exception:
        conn.rollback()
        raise

    # -------------------------------------------------
    # Always close database connection
    # -------------------------------------------------
    finally:
        conn.close()


# -------------------------------------------------
# Get All Orders
# -------------------------------------------------

def get_all_orders() -> list[OrderResponse]:
    """
    Get all orders.
    """
    return []


# -------------------------------------------------
# Get Order By ID
# -------------------------------------------------

def get_order_by_id(order_id: int)-> OrderResponse:
    """
    Get order by ID.
    """
    raise OrderNotFoundException(order_id)