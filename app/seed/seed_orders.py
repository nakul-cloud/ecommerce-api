import random

from app.config.database import get_db_connection

from app.seed.constants import (
    TOTAL_ORDERS,
    MIN_PRODUCTS_PER_ORDER,
    MAX_PRODUCTS_PER_ORDER,
    MIN_QUANTITY,
    MAX_QUANTITY,
    ORDER_STATUSES,
)


def seed_orders():
    """
    Seed the orders and order_items tables with realistic demo data.

    This version never creates negative stock and works with the
    CHECK(stock_quantity >= 0) database constraint.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # --------------------------------------------------
    # Fetch Customers
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE role = 'customer'
        """
    )

    users = cursor.fetchall()

    if not users:
        print("❌ No customers found.")
        conn.close()
        return

    total_orders_created = 0
    total_order_items = 0

    # --------------------------------------------------
    # Create Orders
    # --------------------------------------------------

    for _ in range(TOTAL_ORDERS):

        customer = random.choice(users)
        status = random.choice(ORDER_STATUSES)

        # --------------------------------------------------
        # Fetch ONLY products that still have stock
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                price,
                stock_quantity
            FROM products
            WHERE stock_quantity > 0
            """
        )

        available_products = cursor.fetchall()

        # Inventory exhausted
        if not available_products:
            print("⚠️ Inventory exhausted. Stopping order generation.")
            break

        # Number of products in this order
        number_of_products = min(
            len(available_products),
            random.randint(
                MIN_PRODUCTS_PER_ORDER,
                MAX_PRODUCTS_PER_ORDER,
            ),
        )

        selected_products = random.sample(
            available_products,
            number_of_products,
        )

        order_items = []
        total_amount = 0.0

        # --------------------------------------------------
        # Build Order
        # --------------------------------------------------

        for product in selected_products:

            max_quantity = min(
                MAX_QUANTITY,
                product["stock_quantity"],
            )

            if max_quantity <= 0:
                continue

            quantity = random.randint(
                MIN_QUANTITY,
                max_quantity,
            )

            subtotal = quantity * product["price"]

            total_amount += subtotal

            order_items.append(
                {
                    "product_id": product["id"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                }
            )

        # Skip empty orders
        if not order_items:
            continue

        # --------------------------------------------------
        # Insert Order
        # --------------------------------------------------

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
                customer["id"],
                status,
                round(total_amount, 2),
            ),
        )

        order_id = cursor.lastrowid

        # --------------------------------------------------
        # Insert Order Items
        # --------------------------------------------------

        for item in order_items:

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
                    item["product_id"],
                    item["quantity"],
                    item["unit_price"],
                ),
            )

            # ----------------------------------------------
            # Safe Stock Update
            # ----------------------------------------------

            cursor.execute(
                """
                UPDATE products
                SET stock_quantity = stock_quantity - ?
                WHERE id = ?
                  AND stock_quantity >= ?
                """,
                (
                    item["quantity"],
                    item["product_id"],
                    item["quantity"],
                ),
            )

            total_order_items += 1

        total_orders_created += 1

    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"✅ Orders Seeded      : {total_orders_created}")
    print(f"✅ Order Items Seeded : {total_order_items}")
    print("=" * 60)


if __name__ == "__main__":
    seed_orders()