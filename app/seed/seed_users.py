from faker import Faker

from app.auth.password import hash_password
from app.config.database import get_db_connection

from app.seed.constants import (
    DEFAULT_ADMIN,
    TOTAL_CUSTOMERS,
)

fake = Faker()


def seed_users():
    """
    Seed the users table with demo users.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    total_users = 0

    # --------------------------------------------------
    # Seed Default Admin
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (DEFAULT_ADMIN["email"],),
    )

    if cursor.fetchone() is None:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                hashed_password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                DEFAULT_ADMIN["username"],
                DEFAULT_ADMIN["email"],
                hash_password(DEFAULT_ADMIN["password"]),
                "admin",
            ),
        )

        total_users += 1

    # --------------------------------------------------
    # Seed Customers
    # --------------------------------------------------

    customers_created = 0

    while customers_created < TOTAL_CUSTOMERS:

        username = fake.unique.user_name()
        email = fake.unique.email()

        # ----------------------------------------------
        # Check Username
        # ----------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if cursor.fetchone() is not None:
            continue

        # ----------------------------------------------
        # Check Email
        # ----------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        if cursor.fetchone() is not None:
            continue

        # ----------------------------------------------
        # Insert Customer
        # ----------------------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                hashed_password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                email,
                hash_password("password123"),
                "customer",
            ),
        )

        customers_created += 1
        total_users += 1

    conn.commit()
    conn.close()

    print(f"✅ Seeded {customers_created} customers.")
    print(f"✅ Total users inserted: {total_users}")


if __name__ == "__main__":
    seed_users()