from datetime import datetime

from app.constants.order_status import (
    PENDING,
    CONFIRMED,
    PROCESSING,
    ORDER_STATUSES,
    VALID_TRANSITIONS,
)
from app.config.database import get_db_connection
from app.exceptions.custom_exceptions import (
    OrderNotFoundException,
    ProductNotFoundException,
    ProductOutOfStockException,
    BadRequestException,
)
from app.schemas.internal_schemas import ValidatedOrderItem
from app.schemas.order_schema import (
    OrderCreate,
    OrderCancelRequest,
    OrderItemResponse,
    OrderResponse,
    PaginationResponse,
    PaginatedOrdersResponse,
    OrderStatusUpdate,
    OrderPackingUpdate,
    PackingChecklist,
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
            user_id=current_user.id,
            username=current_user.username,
        )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_orders(
    current_user: UserResponse,
    page: int,
    limit: int,
) -> PaginatedOrdersResponse:
    """
    Retrieve paginated orders.

    Admin:
        Returns all orders.

    Customer:
        Returns only their own orders.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    offset = (page - 1) * limit

    # -------------------------------------------------
    # Count total records
    # -------------------------------------------------

    if current_user.role == "admin":

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            """
        )

    elif current_user.role == "warehouse":

        # Warehouse sees only their active work queue
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status IN (?, ?)
            """,
            (CONFIRMED, PROCESSING),
        )

    else:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE user_id = ?
            """,
            (current_user.id,),
        )

    total_orders = cursor.fetchone()[0]

    # -------------------------------------------------
    # Fetch paginated orders
    # -------------------------------------------------

    if current_user.role == "admin":

        cursor.execute(
            """
            SELECT
                o.id,
                o.user_id,
                o.status,
                o.total_amount,
                o.created_at,
                u.username,
                o.warehouse_notes,
                o.all_items_verified,
                o.package_weight,
                o.package_dimensions
            FROM orders o
            JOIN users u
                ON o.user_id = u.id
            ORDER BY o.created_at DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                limit,
                offset,
            ),
        )

    elif current_user.role == "warehouse":

        # Warehouse sees only Confirmed and Processing orders
        cursor.execute(
            """
            SELECT
                o.id,
                o.user_id,
                o.status,
                o.total_amount,
                o.created_at,
                u.username,
                o.warehouse_notes,
                o.all_items_verified,
                o.package_weight,
                o.package_dimensions
            FROM orders o
            JOIN users u
                ON o.user_id = u.id
            WHERE o.status IN (?, ?)
            ORDER BY o.created_at ASC
            LIMIT ?
            OFFSET ?
            """,
            (
                CONFIRMED,
                PROCESSING,
                limit,
                offset,
            ),
        )

    else:

        cursor.execute(
            """
            SELECT
                o.id,
                o.user_id,
                o.status,
                o.total_amount,
                o.created_at,
                u.username,
                o.warehouse_notes,
                o.all_items_verified,
                o.package_weight,
                o.package_dimensions
            FROM orders o
            JOIN users u
                ON o.user_id = u.id
            WHERE o.user_id = ?
            ORDER BY o.created_at DESC
            LIMIT ?
            OFFSET ?
            """,
            (
                current_user.id,
                limit,
                offset,
            ),
        )

    rows = cursor.fetchall()

    order_responses: list[OrderResponse] = []

    # -------------------------------------------------
    # Build response
    # -------------------------------------------------

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
            JOIN products p
                ON oi.product_id = p.id
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
                subtotal=round(
                    item["unit_price"] * item["quantity"],
                    2,
                ),
            )
            for item in item_rows
        ]

        created_at_str = row["created_at"]

        if " " in created_at_str and "T" not in created_at_str:
            created_at_str = created_at_str.replace(
                " ",
                "T",
            )

        order_responses.append(
            OrderResponse(
                id=row["id"],
                status=row["status"],
                total_amount=row["total_amount"],
                created_at=datetime.fromisoformat(
                    created_at_str
                ),
                items=items,
                user_id=row["user_id"],
                username=row["username"],
                warehouse_notes=row["warehouse_notes"],
                all_items_verified=bool(row["all_items_verified"]) if row["all_items_verified"] is not None else None,
                package_weight=row["package_weight"],
                package_dimensions=row["package_dimensions"],
            )
        )

    conn.close()

    return PaginatedOrdersResponse(
        pagination=PaginationResponse(
            page=page,
            limit=limit,
            total_records=total_orders,
            total_pages=(total_orders + limit - 1) // limit,
        ),
        orders=order_responses,
    )


def get_order_by_id(
    order_id: int,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Get order by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if current_user.role in ("admin", "warehouse"):
        # Admin and warehouse can look up any order by ID
        cursor.execute(
            """
            SELECT
                o.id,
                o.user_id,
                o.status,
                o.total_amount,
                o.created_at,
                u.username,
                o.warehouse_notes,
                o.all_items_verified,
                o.package_weight,
                o.package_dimensions
            FROM orders o
            JOIN users u
                ON o.user_id = u.id
            WHERE o.id = ?
            """,
            (order_id,),
        )
    else:
        cursor.execute(
            """
            SELECT
                o.id,
                o.user_id,
                o.status,
                o.total_amount,
                o.created_at,
                u.username,
                o.warehouse_notes,
                o.all_items_verified,
                o.package_weight,
                o.package_dimensions
            FROM orders o
            JOIN users u
                ON o.user_id = u.id
            WHERE o.id = ?
            AND o.user_id = ?
            """,
            (
                order_id,
                current_user.id,
            ),
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
        user_id=row["user_id"],
        username=row["username"],
        warehouse_notes=row["warehouse_notes"],
        all_items_verified=bool(row["all_items_verified"]) if row["all_items_verified"] is not None else None,
        package_weight=row["package_weight"],
        package_dimensions=row["package_dimensions"],
    )


def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Update the status of an order (Admin).
    Enforces VALID_TRANSITIONS — no illegal state jumps allowed.
    """
    # 1. Validate target status is a recognised value
    if status_update.status not in ORDER_STATUSES:
        raise BadRequestException(
            f"'{status_update.status}' is not a valid order status."
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    # 2. Fetch current order
    cursor.execute(
        """
        SELECT id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # 3. Enforce transition guard
    current_status = row["status"]
    allowed = VALID_TRANSITIONS.get(current_status, [])
    if status_update.status not in allowed:
        conn.close()
        raise BadRequestException(
            f"Cannot transition from '{current_status}' to "
            f"'{status_update.status}'. "
            f"Allowed next statuses: {allowed or ['none — this is a terminal state']}."
        )

    # 4. Apply the update
    cursor.execute(
        """
        UPDATE orders
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status_update.status, order_id),
    )
    conn.commit()
    conn.close()

    # 5. Return the refreshed order
    return get_order_by_id(order_id, current_user)


# ==================================================
# Phase 1 — Customer Cancel Order
# ==================================================

def cancel_order(
    order_id: int,
    cancel_request: OrderCancelRequest,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Cancel a Pending order.
    - Customer: can only cancel their own orders.
    - Validates the order is still Pending.
    - Restores stock for each order item.
    - Records cancelled_at and cancelled_reason.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch order — must exist AND belong to this customer
    cursor.execute(
        """
        SELECT id, user_id, status
        FROM orders
        WHERE id = ? AND user_id = ?
        """,
        (order_id, current_user.id),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # 2. Guard: only Pending orders can be cancelled
    if row["status"] != PENDING:
        conn.close()
        raise BadRequestException(
            f"Order #{order_id} cannot be cancelled — "
            f"it is already '{row['status']}'. "
            "Only Pending orders can be cancelled."
        )

    # 3. Restore stock for each item
    cursor.execute(
        """
        SELECT product_id, quantity
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,),
    )
    items = cursor.fetchall()

    for item in items:
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity + ?
            WHERE id = ?
            """,
            (item["quantity"], item["product_id"]),
        )

    # 4. Cancel the order with audit fields
    cursor.execute(
        """
        UPDATE orders
        SET
            status = 'Cancelled',
            cancelled_at = CURRENT_TIMESTAMP,
            cancelled_reason = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (cancel_request.reason, order_id),
    )
    conn.commit()
    conn.close()

    # 5. Return updated order
    return get_order_by_id(order_id, current_user)


# ==================================================
# Phase 2 — Admin Confirm Order
# ==================================================

def confirm_order(
    order_id: int,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Admin confirms a Pending order, moving it to Confirmed.
    Records confirmed_by (admin user id) and confirmed_at.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch order
    cursor.execute(
        """
        SELECT id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # 2. Guard: must be Pending
    if row["status"] != PENDING:
        conn.close()
        raise BadRequestException(
            f"Order #{order_id} cannot be confirmed — "
            f"current status is '{row['status']}'. "
            "Only Pending orders can be confirmed."
        )

    # 3. Confirm with audit
    cursor.execute(
        """
        UPDATE orders
        SET
            status = 'Confirmed',
            confirmed_by = ?,
            confirmed_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (current_user.id, order_id),
    )
    conn.commit()
    conn.close()

    # 4. Return updated order
    return get_order_by_id(order_id, current_user)


# ==================================================
# Phase 3 — Warehouse: Pack Order (Start Packaging)
# ==================================================

def pack_order(
    order_id: int,
    packing_update: OrderPackingUpdate,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Warehouse claims a Confirmed order and starts packaging (picking items).
    Transition: Confirmed → Processing
    Saves warehouse_notes.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch order
    cursor.execute(
        """
        SELECT id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # 2. Guard: must be Confirmed
    if row["status"] != CONFIRMED:
        conn.close()
        raise BadRequestException(
            f"Order #{order_id} cannot be processed for packing — "
            f"current status is '{row['status']}'. "
            "Only Confirmed orders can be packed."
        )

    # 3. Transition
    cursor.execute(
        """
        UPDATE orders
        SET
            status = 'Processing',
            warehouse_notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (packing_update.warehouse_notes, order_id),
    )
    conn.commit()
    conn.close()

    return get_order_by_id(order_id, current_user)


# ==================================================
# Phase 3 — Warehouse: Ready Order (Ready For Shipment)
# ==================================================

def ready_order(
    order_id: int,
    checklist: PackingChecklist,
    current_user: UserResponse,
) -> OrderResponse:
    """
    Warehouse marks a Processing order as packed, verified, and ready for shipment.
    Transition: Processing → Ready For Shipment
    Writes checklist fields (all_items_verified, package_weight, package_dimensions)
    and audit fields (packed_by, packed_at).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch order
    cursor.execute(
        """
        SELECT id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise OrderNotFoundException(order_id)

    # 2. Guard: must be Processing
    if row["status"] != PROCESSING:
        conn.close()
        raise BadRequestException(
            f"Order #{order_id} cannot be marked ready — "
            f"current status is '{row['status']}'. "
            "Only Processing orders can be marked ready for shipment."
        )

    # 3. Transition with packing details & audit
    cursor.execute(
        """
        UPDATE orders
        SET
            status = 'Ready For Shipment',
            packed_by = ?,
            packed_at = CURRENT_TIMESTAMP,
            all_items_verified = ?,
            package_weight = ?,
            package_dimensions = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            current_user.id,
            checklist.all_items_verified,
            checklist.package_weight,
            checklist.package_dimensions,
            order_id,
        ),
    )
    conn.commit()
    conn.close()

    return get_order_by_id(order_id, current_user)