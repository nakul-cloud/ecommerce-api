from app.config.database import get_db_connection


def reset_database():
    """
    Remove all records from the database.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete child tables first
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")

    # Reset SQLite AUTOINCREMENT counters
    cursor.execute("DELETE FROM sqlite_sequence")

    conn.commit()
    conn.close()

    print("✅ Database reset successfully.")


if __name__ == "__main__":
    reset_database()