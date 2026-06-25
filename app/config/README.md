# `app/config/` — Configuration & Infrastructure Setup

This folder acts as the foundation of our application, housing settings, environment loader configuration, and base database setup logic.

---

## 1. Purpose

> Why do we have a config folder?

In professional backend engineering, code should be **decoupled** from settings and environment-specific database handlers. The `config/` folder exists to:
- **Centralize application configuration**: Ensure every part of the application reads settings from a single source of truth.
- **Isolate environment details**: Keep database file paths, names, and security keys out of the main code.
- **Initialize database connection logic**: Establish database connection utilities and handles in one spot.

If you don't use a configuration folder, you end up repeating database connection code in multiple files and hardcoding database paths or API credentials directly in your business logic. That leads to security risks and bugs when deploying to staging or production environments.

---

## 2. Responsibilities

### What belongs inside `config/`

- Reading and parsing `.env` files.
- Application-wide configuration class definitions (like app title, version, secret keys).
- Global database connection helpers (`get_db_connection()`).
- Database initialization and table definitions (`create_tables()`).

### What does NOT belong inside `config/`

- Business logic or validations.
- Specific database operations (like inserting a product, updating stock).
- Route declarations.

---

## 3. Files

### `settings.py`

- **Purpose**: Loads environment variables from the `.env` file and makes them accessible to other Python modules.
- **Functions/Variables**:
  - `load_dotenv()`: Reads the `.env` file at the root.
  - `APP_NAME`: Name of the application (defaults to `"E-Commerce API"`).
  - `APP_VERSION`: Current API version (defaults to `"1.0.0"`).
  - `DATABASE_PATH`: Local database storage location (defaults to `"data/ecommerce.db"`).
  - `ADMIN_API_KEY`: API key for administrative operations (defaults to `"admin123"`).
- **When is it called**: Imported and executed as soon as the app starts up and other modules need settings.
- **Who calls it**: `app/main.py`, `app/config/database.py`, and any controllers/routes needing settings.

### `database.py`

- **Purpose**: Manages the SQLite database connection lifecycle and initial table structures.
- **Functions**:
  - `get_db_connection()`: Establishes and returns an active connection to SQLite, with rows formatted as dictionary-like objects (`Row`).
  - `create_tables()`: Runs the SQL scripts to create `products`, `orders`, and `order_items` tables if they don't exist yet.
- **When is it called**: `get_db_connection()` is called on demand by controllers for database queries. `create_tables()` runs once during the FastAPI startup event.
- **Who calls it**: `app/main.py` (during startup) and controllers like `product_controller.py`.

---

## 4. Request Flow

The config layer is accessed by the application startup handler and the controllers:

```
                  [App Startup]
                        │
                        ▼
            ┌───────────────────────┐
            │   config/database.py  │  ← Runs create_tables()
            └───────────────────────┘
                        │
                        ▼
                  [Request Flow]
                        │
                        ▼
    Client ──► Route ──► Controller ──► config/database.py (get_db_connection)
                                                 │
                                                 ▼
                                           SQLite Database
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

The `config` folder is where the database connection is set up and application settings are configured. Think of it as the building's electrical room and plumbing hub. If you need to change the database path, add a new API credential, or modify table structures, this is the only place you need to touch.

---

## 6. Real-World Analogy

- **`settings.py`** = The Control Panel / Thermostat settings.
- **`database.py`** = The Main Water valve and pipes that connect the house to the municipal reservoir.

---

## 7. Best Practices

### Do

- Use default values in `settings.py` in case `.env` is missing.
- Keep database schema definitions clean and commented.
- Always close database connections in a `finally` block or context manager.

### Don't

- Hardcode secrets directly inside Python files.
- Run database query executions in `settings.py`.
- Commit the `.env` file to git.

### Common Mistakes

- Forgetting to close SQLite connections, causing file locking issues (`WinError 32` or database locks).
- Changing column names in `database.py` but failing to drop the existing database file, which prevents new tables from being created.

---

## 8. Interview Questions

1. **Why separate configuration (`settings.py`) from database logic (`database.py`)?**
   To follow the Single Responsibility Principle. `settings.py` is responsible only for reading variables, whereas `database.py` manages connections and structures.
2. **What does `sqlite3.Row` do?**
   It allows you to access database columns by name (like `row['price']`) rather than indices (like `row[4]`), making code much more readable and robust.
3. **What is `dotenv` and why is it useful?**
   It loads key-value pairs from a `.env` file into system environment variables so you can access them using `os.getenv()`.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Direct SQLite module calls.
- Manual connection creation.
- Hardcoded DDL queries.

### Future Evolution
- **Phase 4**: Replace direct `sqlite3` connection code with SQLAlchemy database engines and session makers.
- **Phase 4**: Replace raw string SQL queries with Alembic migration scripts.

---

## 30-Second Revision

- `config/` manages app settings and database connections.
- `settings.py` loads variables from `.env` using `python-dotenv`.
- `database.py` provides `get_db_connection()` and builds database schemas.
- SQLite connections use `sqlite3.Row` for key-based column access.
- Changing schema requires dropping the local `.db` file or running migrations since `CREATE TABLE IF NOT EXISTS` won't update existing tables.
