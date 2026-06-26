# `data/` — Database & Persistence Layer

> The physical storage layer hosting our local relational database files, mapping out schema persistence, and defining transactional state.

---

## 1. Purpose

In this phase of the E-Commerce API, we use **SQLite** as our relational database management system (RDBMS). The `data/` directory is the physical home of this database. 

While SQLite is a lightweight, serverless database, we treat it with the same architectural discipline as a full-scale PostgreSQL database:
- **Environment Isolation**: Database files are stored locally and excluded from git control to ensure local development environments do not pollute each other.
- **Physical Segregation**: Keeping database files in a designated directory isolates persistent files from application source code, facilitating cleaner packaging and deployment pipelines.
- **Dynamic Initialization**: Rather than committing pre-populated binary files, the tables are generated dynamically at runtime on application startup.

---

## 2. SQLite Architecture & Lifecycle

Although SQLite is file-based, it behaves as a robust ACID-compliant relational engine. Understanding how it operates in the context of an ASGI web framework like FastAPI is critical:

```
                  ┌───────────────────────────────┐
                  │   FastAPI Web Workers (ASGI)  │
                  └───────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
    Thread Worker 1        Thread Worker 2        Thread Worker 3
          │                       │                       │
          └───────────┬───────────┴───────────┬───────────┘
                      │                       │
                      │ (check_same_thread=False)
                      ▼                       ▼
               ┌─────────────┐         ┌─────────────┐
               │ Connection  │         │ Connection  │
               └─────────────┘         └─────────────┘
                      │                       │
                      ▼                       ▼
         ┌─────────────────────────────────────────────────┐
         │              SQLite Database Engine             │
         └─────────────────────────────────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         │              Physical File Locking              │
         ▼                                                 ▼
┌──────────────────┐                              ┌──────────────────┐
│   ecommerce.db   │                              │ ecommerce.db-wal │
│  (Main Database) │                              │ (Write-Ahead Log)│
└──────────────────┘                              └──────────────────┘
```

### Key Concurrency Mechanics

1. **The Concurrency Challenge**: SQLite allows multiple readers simultaneously, but only **one writer** at a time. When a write transaction begins, SQLite locks the entire database file.
2. **`check_same_thread=False`**: By default, Python's `sqlite3` driver restricts connection objects to the thread that created them. Since FastAPI runs route handlers asynchronously across multiple thread pool workers, we pass `check_same_thread=False` in [database.py](file:///d:/ecommerce-api/app/config/database.py) to let FastAPI share connections across threads safely, provided we manage transaction lifecycles carefully.
3. **Write-Ahead Logging (WAL)**: In advanced setups, SQLite uses WAL mode (`ecommerce.db-wal`) where writes are written to a append-only log file rather than directly blocking reader access to the main database file. This increases concurrency significantly.

---

## 3. Files

### `ecommerce.db`
The primary SQLite database file. It contains the following tables:
* **`users`**: Customer and Admin accounts with hashed passwords and permission roles.
* **`products`**: Inventory records including name, description, price, stock, and cost margins.
* **`orders`**: Transaction records containing ordering customer details and timestamps.
* **`order_items`**: One-to-many relationship rows binding orders to individual products, quantities, and historical unit prices.

> [!CAUTION]
> This file is explicitly listed in `.gitignore` and must **never** be committed to version control. Committing it would cause merge conflicts, overwrite teammate data, and expose development credentials.

---

## 4. Real-World Analogy

Think of the `data/` folder as the **physical warehouse filing cabinet**:
* The **API source code** is the set of office instructions on how to handle orders.
* The **FastAPI app** is the staff executing those instructions.
* The **`ecommerce.db` file** is the filing cabinet. Even if the entire staff goes home at night (server shutdown), the filing cabinet keeps the paper records safe. If you modify the cabinet directly without going through the office staff, you risk making a mess of the files.

---

## 5. Interview Questions & Tips

### 1. What are the limitations of SQLite in a production environment?
* **Write Lock Contention**: SQLite locks the whole database file during writes. In high-traffic environments with hundreds of concurrent writes per second, it will raise `sqlite3.OperationalError: database is locked`.
* **No Network Interface**: It cannot be accessed over a network, making it impossible to scale horizontally with multiple application servers pointing to the same database server.
* **Feature Set**: Lacks native support for advanced indexing types (e.g., GIN, GiST), schema schemas, and sophisticated user/role management.

### 2. How do you handle database migrations in a production API?
Instead of dropping the database, we use migration tools like **Alembic** (for SQLAlchemy) or **Flyway/Liquibase**. Migration tools track versioned schema changes in incremental migration scripts (e.g., `v1_add_user_roles.sql`), allowing us to alter tables, add indexes, and seed data across environments without losing existing production data.

### 3. What is the purpose of foreign key constraints, and are they enabled by default in SQLite?
Foreign keys enforce referential integrity between tables (e.g., preventing an `order_item` from referencing a non-existent `product`). 
**Crucial SQLite Gotcha**: In SQLite, foreign key enforcement is **disabled by default** for backward compatibility. You must explicitly execute `PRAGMA foreign_keys = ON;` on every database connection open, otherwise database-level cascades and constraints will be silently ignored.

---

## 6. 30-Second Revision

- **`data/`** holds the binary SQLite database files (`ecommerce.db`).
- **File Locks**: SQLite is highly concurrent for reads but locks the file for writes.
- **Git Safety**: Always exclude the database from git using `.gitignore`.
- **Runtime Init**: Tables are automatically built on first start via SQL commands inside config files.
- **Scaling Path**: Perfect for prototyping; will be migrated to PostgreSQL using Alembic in later phases.
