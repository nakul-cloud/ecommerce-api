import os
import sqlite3
from app.config.settings import DATABASE_PATH
from app.utils.logger import logger


def get_db_connection():
    """
    Create and return SQLite connection.
    """
    logger.info(f"DATABASE_PATH: {DATABASE_PATH}")
    logger.info(f"ABSOLUTE PATH: {os.path.abspath(DATABASE_PATH)}")

    conn = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():
    """
    Create all application tables if they do not exist.
    """

    conn = get_db_connection()

    cursor = conn.cursor()

    # ==========================
    # Products Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
                CHECK(stock_quantity >= 0),
            cost_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ==========================
    # Users Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,

        email TEXT NOT NULL UNIQUE,

        hashed_password TEXT NOT NULL,

        role TEXT NOT NULL DEFAULT 'customer',

        is_active BOOLEAN NOT NULL DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    # ==========================
    # Orders Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # ==========================
    # Order Items Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,

            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)



    conn.commit()
    conn.close()

    logger.info("Database tables created successfully.")

    # Run column migrations after tables are guaranteed to exist
    run_migrations()


def run_migrations():
    """
    Safely add new columns to existing tables.

    Uses try/except to silently skip columns that already exist.
    SQLite does not support IF NOT EXISTS on ALTER TABLE.
    This pattern is safe to run on every startup.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # -----------------------------------------------
    # Phase 1 & 2 — Order audit columns
    # -----------------------------------------------

    migrations = [
        # Phase 1 — Cancellation audit
        "ALTER TABLE orders ADD COLUMN cancelled_at TIMESTAMP",
        "ALTER TABLE orders ADD COLUMN cancelled_reason TEXT",

        # Phase 2 — Admin confirmation audit
        "ALTER TABLE orders ADD COLUMN confirmed_by INTEGER REFERENCES users(id)",
        "ALTER TABLE orders ADD COLUMN confirmed_at TIMESTAMP",

        # Phase 3 — Warehouse packing audit
        "ALTER TABLE orders ADD COLUMN packed_by INTEGER REFERENCES users(id)",
        "ALTER TABLE orders ADD COLUMN packed_at TIMESTAMP",
        "ALTER TABLE orders ADD COLUMN warehouse_notes TEXT",
        "ALTER TABLE orders ADD COLUMN all_items_verified BOOLEAN",
        "ALTER TABLE orders ADD COLUMN package_weight REAL",
        "ALTER TABLE orders ADD COLUMN package_dimensions TEXT",
    ]

    for sql in migrations:
        try:
            cursor.execute(sql)
            logger.info(f"Migration applied: {sql}")
        except Exception:
            # Column already exists — safe to ignore
            pass

    conn.commit()
    conn.close()

    logger.info("Database migrations complete.")