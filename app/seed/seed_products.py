import random

from app.config.database import get_db_connection

from app.seed.constants import (
    PRODUCT_CATEGORIES,
    PRODUCT_VARIANTS,
    TOTAL_PRODUCTS,
)

from app.seed.utils import (
    random_price,
    random_cost_price,
    random_stock,
    random_description,
)


def seed_products():
    """
    Seed the products table with realistic demo products.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    generated_names = set()
    total_products = 0

    # --------------------------------------------------
    # Generate Products
    # --------------------------------------------------

    while total_products < TOTAL_PRODUCTS:

        # Random category
        category = random.choice(
            list(PRODUCT_CATEGORIES.keys())
        )

        category_data = PRODUCT_CATEGORIES[category]

        # Random brand
        brand = random.choice(
            category_data["brands"]
        )

        # Random product
        product = random.choice(
            category_data["products"]
        )

        # Random variant
        variant = random.choice(
            PRODUCT_VARIANTS
        )

        # Product Name
        product_name = f"{brand} {product} {variant}"

        # Skip duplicates in current run
        if product_name in generated_names:
            continue

        generated_names.add(product_name)

        # Skip duplicates already in database
        cursor.execute(
            """
            SELECT id
            FROM products
            WHERE name = ?
            """,
            (product_name,),
        )

        if cursor.fetchone():
            continue

        # ------------------------------------------
        # Price
        # ------------------------------------------

        min_price, max_price = category_data["price_range"]

        price = random_price(
            min_price,
            max_price,
        )

        cost_price = random_cost_price(
            price,
        )

        # ------------------------------------------
        # Stock
        # Generate realistic inventory
        # ------------------------------------------

        stock = random_stock(
            minimum=20,
            maximum=200,
        )

        # ------------------------------------------
        # Description
        # ------------------------------------------

        description = random_description()

        # ------------------------------------------
        # Insert Product
        # ------------------------------------------

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
                product_name,
                description,
                category,
                price,
                stock,
                cost_price,
            ),
        )

        total_products += 1

    conn.commit()
    conn.close()

    print("=" * 50)
    print(f"✅ Products Seeded : {total_products}")
    print("=" * 50)


if __name__ == "__main__":
    seed_products()