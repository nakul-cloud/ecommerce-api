from datetime import datetime

from app.constants.order_status import PENDING
from app.config.database import get_db_connection
from app.exceptions.custom_exceptions import (
    OrderNotFoundException,
    ProductNotFoundException,
    ProductOutOfStockException,
)
from app.schemas.internal_schemas import ValidatedOrderItem
from app.schemas.order_schema import (
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
)
from app.schemas.user_schema import UserResponse


def create_order(
    order: OrderCreate,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Create a new order for the currently authenticated user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    total_amount = 0.0
    validated_products: list[ValidatedOrderItem] = []

    try:
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

            if product is None:
                raise ProductNotFoundException(item.product_id)

            if product["stock_quantity"] < item.quantity:
                raise ProductOutOfStockException(item.product_id)

            subtotal = round(product["price"] * item.quantity, 2)
            total_amount = round(total_amount + subtotal, 2)

            validated_products.append(
                ValidatedOrderItem(
                    product_id=product["id"],
                    product_name=product["name"],
                    quantity=item.quantity,
                    unit_price=product["price"],
                    subtotal=subtotal,
                )
            )

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
                PENDING,
                total_amount,
            ),
        )

        order_id = cursor.lastrowid

        for product in validated_products:
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

            if cursor.rowcount == 0:
                raise ProductOutOfStockException(product.product_id)

        conn.commit()

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

        response_items = [
            OrderItemResponse(
                product_id=product.product_id,
                product_name=product.product_name,
                quantity=product.quantity,
                unit_price=product.unit_price,
                subtotal=product.subtotal,
            )
            for product in validated_products
        ]

        return OrderResponse(
            id=order_id,
            status=created_order["status"],
            total_amount=total_amount,
            created_at=datetime.fromisoformat(created_order["created_at"]),
            items=response_items,
        )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_all_orders() -> list[OrderResponse]:
    """
    Get all orders.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            status,
            total_amount,
            created_at
        FROM orders
        ORDER BY id
        """
    )
    rows = cursor.fetchall()

    order_responses = []
    for row in rows:
        order_id = row["id"]
        cursor.execute(
            """
            SELECT
                oi.product_id,
                p.name AS product_name,
                oi.quantity,
                oi.unit_price
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
            """,
            (order_id,),
        )
        item_rows = cursor.fetchall()

        items = [
            OrderItemResponse(
                product_id=item["product_id"],
                product_name=item["product_name"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                subtotal=round(item["unit_price"] * item["quantity"], 2),
            )
            for item in item_rows
        ]

        created_at_str = row["created_at"]
        if " " in created_at_str and "T" not in created_at_str:
            created_at_str = created_at_str.replace(" ", "T")

        order_responses.append(
            OrderResponse(
                id=order_id,
                status=row["status"],
                total_amount=row["total_amount"],
                created_at=datetime.fromisoformat(created_at_str),
                items=items,
            )
        )

    conn.close()
    return order_responses


def get_order_by_id(order_id: int) -> OrderResponse:
    """
    Get order by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            status,
            total_amount,
            created_at
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    cursor.execute(
        """
        SELECT
            oi.product_id,
            p.name AS product_name,
            oi.quantity,
            oi.unit_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
        """,
        (order_id,),
    )
    item_rows = cursor.fetchall()
    conn.close()

    items = [
        OrderItemResponse(
            product_id=item["product_id"],
            product_name=item["product_name"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=round(item["unit_price"] * item["quantity"], 2),
        )
        for item in item_rows
    ]

    created_at_str = row["created_at"]
    if " " in created_at_str and "T" not in created_at_str:
        created_at_str = created_at_str.replace(" ", "T")

    return OrderResponse(
        id=row["id"],
        status=row["status"],
        total_amount=row["total_amount"],
        created_at=datetime.fromisoformat(created_at_str),
        items=items,
    )
