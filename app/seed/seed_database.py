"""
Master database seeder.

Run:

python -m app.seed.seed_database
"""

from app.seed.reset_database import reset_database
from app.seed.seed_users import seed_users
from app.seed.seed_products import seed_products
from app.seed.seed_orders import seed_orders


def seed_database():
    """
    Reset and seed the complete database.
    """

    print("=" * 60)
    print("🌱 E-Commerce Database Seeder")
    print("=" * 60)

    # --------------------------------------------------
    # Reset Database
    # --------------------------------------------------

    print("\n🗑 Resetting Database...")
    reset_database()

    # --------------------------------------------------
    # Seed Users
    # --------------------------------------------------

    print("\n👤 Seeding Users...")
    seed_users()

    # --------------------------------------------------
    # Seed Products
    # --------------------------------------------------

    print("\n📦 Seeding Products...")
    seed_products()

    # --------------------------------------------------
    # Seed Orders
    # --------------------------------------------------

    print("\n🛒 Seeding Orders...")
    seed_orders()

    print("\n" + "=" * 60)
    print("🎉 Database Seeded Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    seed_database()