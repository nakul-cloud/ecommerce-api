# `data/` — Database Storage

> Contains the SQLite database file. Auto-created on first startup, excluded from version control.

## Files

### `ecommerce.db`

The SQLite database storing `products`, `orders`, and `order_items` tables. Created automatically by `create_tables()` in `app/config/database.py` when the server starts.

> [!CAUTION]
> This file is listed in `.gitignore` and should **never** be committed. It contains local development data and would cause merge conflicts.

## Real-World Analogy

`data/` = **The warehouse filing cabinet**. Code lives in the office. Data lives in the warehouse.

## 30-Second Revision

- `data/` holds SQLite `.db` files — auto-created on startup
- Excluded from Git via `.gitignore`
- In production (Phase 4+), SQLite will be replaced by PostgreSQL
