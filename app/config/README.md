# `app/config/` — Configuration & Database Setup

> Centralizes application settings and database infrastructure. Change database paths, API keys, or table schemas here — nowhere else.

## Files

### `settings.py`

Loads environment variables from the `.env` file using `python-dotenv` and exposes them as module-level constants.

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `"E-Commerce API"` | Application title shown in Swagger docs |
| `APP_VERSION` | `"1.0.0"` | API version string |
| `DATABASE_PATH` | `"data/ecommerce.db"` | Path to the SQLite database file |
| `ADMIN_API_KEY` | `"admin123"` | API key for admin operations |

> [!CAUTION]
> Never hardcode secrets in Python files. Always use `.env` for API keys and credentials. The `.env` file is excluded from Git via `.gitignore`.

### `database.py`

Manages SQLite connections and table creation.

| Function | Purpose | Called By |
|---|---|---|
| `get_db_connection()` | Returns an active SQLite connection with `Row` factory | Controllers |
| `create_tables()` | Creates `products`, `orders`, `order_items` tables if they don't exist | `main.py` on startup |

### `dependencies.py`

Contains reusable FastAPI dependencies, specifically for request security and validation.

| Function / Dependency | Purpose | Header Required |
|---|---|---|
| `verify_admin_api_key()` | Validates client API key against the configured admin key | `X-API-Key` |

> [!IMPORTANT]
> **FastAPI Dependency Injection (`Depends`)**:
> Using `Depends` decouples our authentication logic from our route functions. The route handler declares the dependency, and FastAPI resolves it before invoking the function. If validation fails (e.g., invalid/missing API key), FastAPI immediately returns a `401 Unauthorized` response without running the route's body.

> [!WARNING]
> `CREATE TABLE IF NOT EXISTS` will **not** update existing tables. If you add a column to the schema, you must delete `data/ecommerce.db` and restart the server (or use migrations).

## Request Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'nodeTextColor': '#1e293b', 'textColor': '#ffffff', 'titleColor': '#ffffff', 'edgeLabelBackground': '#1e293b', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#e2e8f0', 'actorBkg': '#f8fafc', 'actorBorder': '#cbd5e1', 'actorTextColor': '#1e293b', 'signalColor': '#4f46e5', 'signalTextColor': '#ffffff', 'noteBkgColor': '#fef08a', 'noteBorderColor': '#facc15', 'noteTextColor': '#713f12'}}}%%
flowchart TD
    subgraph StartupFlow [App Startup Flow]
        direction TB
        S1[App Startup] --> S2[app/main.py]
        S2 -->|Calls| S3[config/database.py: create_tables]
        S3 -->|Initializes| S4[(SQLite DB File)]
    end

    subgraph RequestFlow [Active Request Flow]
        direction TB
        R1[Controller Action] -->|1. Calls| R2[config/database.py: get_db_connection]
        R2 -->|2. Returns Connection| R3[Active Connection]
        R3 -->|3. Query / Update| R4[(SQLite DB File)]
    end
    
    style S3 fill:#4f46e5,stroke:#3730a3,color:#ffffff
    style R2 fill:#4f46e5,stroke:#3730a3,color:#ffffff
```

## Real-World Analogy

- `settings.py` = The control panel / thermostat settings
- `database.py` = The plumbing system connecting the building to the water supply

## Best Practices

**Do:** Use default values in `os.getenv()` so the app runs even without a `.env` file.
**Don't:** Commit `.env` to Git. Don't run business queries inside `settings.py`.

## 30-Second Revision

- `settings.py` loads variables from `.env` using `python-dotenv`
- `database.py` provides `get_db_connection()` and `create_tables()`
- `dependencies.py` implements reusable route dependencies like administrative API key validation via FastAPI `Depends()`
- `sqlite3.Row` lets you access columns by name (`row["price"]`) instead of index
- Changing table schemas requires deleting the `.db` file or running migrations
