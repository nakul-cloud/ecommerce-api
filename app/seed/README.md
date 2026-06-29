# `app/seed/` — Database Seeding Module

> Programmatic data seeder for populating the database with realistic demo data for development and testing.

---

## 1. Purpose

The seed module provides a repeatable, automated way to fill the database with realistic demo data. Instead of manually inserting products and users via the API, you can run a single command to generate hundreds of records instantly.

This is essential for:
- **Development**: Immediately have data to work with after cloning the repo.
- **Testing**: Reproduce consistent states (same 100 users, 250 products, 1000 orders) for manual or automated tests.
- **Portfolio Demos**: Show realistic-looking data when presenting the API.

---

## 2. How to Run

```bash
# From the project root with venv activated
python -m app.seed.seed_database
```

This command will:
1. **Reset** all tables (wipes existing rows and resets auto-increment counters)
2. **Seed Users** — 1 default admin + 100 faker-generated customers
3. **Seed Products** — 250 products across 10 real-world categories
4. **Seed Orders** — 1000 orders with 1–6 random products each

**Default Admin Credentials** (created by the seeder):
```
Email:    admin@example.com
Password: admin123
```

---

## 3. Files

### `seed_database.py`
Master orchestrator. Calls reset → seed_users → seed_products → seed_orders in order. Run this to seed everything in one shot.

### `reset_database.py`
Deletes all rows from `order_items`, `orders`, `products`, `users` in the correct FK order, then resets SQLite `AUTOINCREMENT` counters by clearing `sqlite_sequence`. This ensures IDs restart from 1 on every seed run.

### `seed_users.py`
Creates the default admin account (if not already present) and generates `TOTAL_CUSTOMERS` (100) fake customer accounts using the `Faker` library. Each customer gets a unique username, unique email, and the default password `password123`.

### `seed_products.py`
Generates `TOTAL_PRODUCTS` (250) products. Each product is built from a random combination of:
- **Category** (e.g., Electronics, Laptops, Gaming)
- **Brand** (e.g., Sony, Dell, Razer)
- **Product name** (e.g., Smart TV, ThinkPad, Gaming Mouse)
- **Variant** (e.g., Pro, Ultra, Series X)

Prices are randomized within realistic category ranges (e.g., Laptops: ₹35,000–₹2,50,000). Cost prices are derived from selling price using `MIN_COST_PERCENTAGE` (0.55) to `MAX_COST_PERCENTAGE` (0.82).

### `seed_orders.py`
Generates `TOTAL_ORDERS` (1000) orders. Each order:
- Is assigned to a random existing customer
- Contains 1–6 random products with quantity 1–4 each
- Records the `unit_price` at time of purchase (snapshot pricing)
- Assigns a random `status`: Pending, Processing, Shipped, or Delivered
- Deducts stock from the products table

### `constants.py`
Central configuration for all seeder parameters:

| Constant | Value | Description |
|---|---|---|
| `TOTAL_CUSTOMERS` | 100 | Number of customer accounts to create |
| `TOTAL_PRODUCTS` | 250 | Number of product records to generate |
| `TOTAL_ORDERS` | 1000 | Number of orders to place |
| `MIN_PRODUCTS_PER_ORDER` | 1 | Minimum line items per order |
| `MAX_PRODUCTS_PER_ORDER` | 6 | Maximum line items per order |
| `MIN_COST_PERCENTAGE` | 0.55 | Minimum cost as a fraction of selling price |
| `MAX_COST_PERCENTAGE` | 0.82 | Maximum cost as a fraction of selling price |
| `ORDER_STATUSES` | Pending, Processing, Shipped, Delivered | Possible order statuses |

### `utils.py`
Shared helper functions used by the individual seeders:
- `random_price(min, max)` — Returns a rounded float between two bounds
- `random_cost_price(selling_price)` — Derives a realistic cost price
- `random_stock(min, max)` — Returns a random integer for stock quantity
- `random_description()` — Generates 3-sentence product descriptions via Faker
- `random_quantity(min, max)` — Returns a random order quantity
- `random_choice(items)` — Picks one random element from a list
- `random_sample(items, count)` — Picks N unique elements from a list

---

## 4. Dependencies

The seed module requires `Faker` to generate realistic names, emails, and text. Install it with:

```bash
pip install faker
```

> [!NOTE]
> `faker` is a dev dependency only. It should not be included in production deployments. Consider separating it into a `requirements-dev.txt`.

---

## 5. Design Decisions

| Decision | Why |
|---|---|
| **Delete child tables first in reset** | `order_items` references `orders` and `products`. SQLite FK constraints require deleting child rows before parent rows to avoid constraint violations. |
| **Reset `sqlite_sequence`** | Clears AUTOINCREMENT counters so IDs restart at 1 on every seed run. Ensures predictable IDs in tests and demos. |
| **Snapshot pricing in orders** | `order_items.unit_price` records the price at time of order creation. This means future product price changes do not alter historical order totals — matching real e-commerce behavior. |
| **Skip duplicate users** | The seeder checks for existing usernames and emails before inserting to prevent UNIQUE constraint violations during partial re-runs. |

---

## 6. 30-Second Revision

- Run `python -m app.seed.seed_database` to reset and repopulate the entire database.
- Default admin: `admin@example.com` / `admin123`.
- Customer default password: `password123`.
- Constants for all counts and ranges live in `constants.py`.
- `Faker` generates realistic names, emails, and descriptions.
