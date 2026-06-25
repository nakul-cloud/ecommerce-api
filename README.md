# E-Commerce API

A production-quality REST API for an e-commerce platform, built with **FastAPI** and **SQLite**.

This project is designed as a learning path for professional backend engineering. Every architectural decision here mirrors what you'd see in real companies — just scaled down so you can understand *why* things are built this way before dealing with the complexity of large systems.

---

## Why This Project Exists

Most tutorials teach you FastAPI syntax. This project teaches you **backend architecture**.

By the end of this project, you will understand:

- How to structure a real backend project (not just a single `main.py` file)
- Why we separate routes, controllers, schemas, and config
- How request validation works before your code even runs
- How to handle errors professionally instead of crashing the server
- How middleware intercepts every request
- How to evolve from raw SQL to ORM to production patterns

---

## Features Implemented

### Phase 1 — Foundation (Current)

- [x] Project structure following industry conventions
- [x] FastAPI app with versioned configuration
- [x] SQLite database with auto-creating tables on startup
- [x] Environment-based configuration (`.env` file)
- [x] Pydantic schemas with validation rules
- [x] Product CRUD operations (Create, List, Retrieve, Delete)
- [x] Separate routes, controllers, and schemas
- [x] Order schema definitions

### Coming Next

- [ ] Product Update CRUD operation
- [ ] Order creation with stock validation
- [ ] Custom exception handling
- [ ] Request timing middleware
- [ ] Utility functions and constants
- [ ] Automated tests


---

## Architecture

### The Big Picture

This project follows a **layered architecture**. Each layer has one job, and layers only talk to the layer directly below them.

```
┌─────────────────────────────────────────┐
│              CLIENT (Browser / Postman)  │
└──────────────────┬──────────────────────┘
                   │ HTTP Request
                   ▼
┌─────────────────────────────────────────┐
│              MIDDLEWARE                  │
│  (timing.py — logs request duration)    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              ROUTES                     │
│  (products.py, orders.py)               │
│  Defines endpoints, delegates work      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              CONTROLLERS                │
│  (product_controller.py)                │
│  Business logic, DB operations          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              DATABASE                   │
│  (SQLite via database.py)               │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              RESPONSE                   │
│  (Filtered through ProductResponse)     │
└─────────────────────────────────────────┘
```

### Request Lifecycle — What Happens When You Hit `POST /products`

```
1. Client sends POST /products with JSON body

2. FastAPI receives the request
   ↓
3. Middleware runs (timing, logging — not yet implemented)
   ↓
4. Route matched → products.py → create_new_product()
   ↓
5. Pydantic validates the request body using ProductCreate schema
   → If invalid: 422 Unprocessable Entity returned immediately
   → If valid: continues
   ↓
6. Route calls controller → product_controller.create_product()
   ↓
7. Controller opens DB connection, executes INSERT query
   ↓
8. Controller builds ProductResponse (hides cost_price from client)
   ↓
9. FastAPI serializes response to JSON, sends 201 Created
```

---

## Project Structure

```
ecommerce-api/
│
├── app/                          # All application code lives here
│   ├── __init__.py               # Makes 'app' a Python package
│   ├── main.py                   # FastAPI app creation and startup
│   │
│   ├── config/                   # Configuration and database setup
│   │   ├── settings.py           # Environment variables (app name, DB path, API keys)
│   │   └── database.py           # SQLite connection + table creation
│   │
│   ├── routes/                   # API endpoint definitions
│   │   ├── products.py           # /products endpoints
│   │   └── orders.py             # /orders endpoints (placeholder)
│   │
│   ├── controllers/              # Business logic layer
│   │   ├── product_controller.py # Product CRUD operations
│   │   └── order_controller.py   # Order operations (placeholder)
│   │
│   ├── schemas/                  # Request/response validation models
│   │   ├── product_schema.py     # ProductCreate, ProductUpdate, ProductResponse
│   │   └── order_schema.py       # OrderItem, OrderCreate, OrderResponse
│   │
│   ├── exceptions/               # Error handling (placeholder)
│   │   ├── custom_exceptions.py  # Custom exception classes
│   │   └── handlers.py           # Global exception handlers
│   │
│   ├── middleware/               # Request/response interceptors (placeholder)
│   │   └── timing.py             # Request duration logging
│   │
│   └── utils/                    # Shared utilities (placeholder)
│       ├── constants.py          # App-wide constants
│       └── helpers.py            # Reusable helper functions
│
├── data/                         # SQLite database storage
│   └── ecommerce.db              # Auto-created on first startup
│
├── tests/                        # Test files (coming soon)
│
├── .env                          # Secret configuration (never commit this)
├── .gitignore                    # Files Git should ignore
├── requirements.txt              # Python dependencies
└── README.md                     # You are here
```

---

## Tech Stack

| Technology | Why We Use It |
|---|---|
| **Python 3.11+** | Industry standard for backend + AI/ML work |
| **FastAPI** | Modern, fast, auto-generates docs, built-in validation |
| **Uvicorn** | ASGI server that runs FastAPI apps |
| **SQLite** | Zero-config database, perfect for learning (swap to PostgreSQL later) |
| **Pydantic** | Data validation — catches bad input before it reaches your code |
| **python-dotenv** | Loads secrets from `.env` file so they never touch your code |

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/nakul-cloud/ecommerce-api.git
cd ecommerce-api

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install fastapi uvicorn python-dotenv

# 5. Create a .env file (optional — defaults are built in)
# APP_NAME=E-Commerce API
# APP_VERSION=1.0.0
# DATABASE_PATH=data/ecommerce.db
# ADMIN_API_KEY=your-secret-key

# 6. Run the server
uvicorn app.main:app --reload
```

---

## Running the Project

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload
```

The server starts at: **http://127.0.0.1:8000**

---

## Swagger Documentation

FastAPI auto-generates interactive API docs. Once the server is running:

| URL | What It Is |
|---|---|
| http://127.0.0.1:8000/docs | **Swagger UI** — interactive, try endpoints directly |
| http://127.0.0.1:8000/redoc | **ReDoc** — cleaner read-only documentation |

---

## API Endpoints

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a welcome message confirming the API is running |

### Products

| Method | Endpoint | Description | Status |
|---|---|---|---|
| `POST` | `/products` | Create a new product | Implemented |
| `GET` | `/products` | List all products | Implemented |
| `GET` | `/products/{product_id}` | Get a single product | Implemented |
| `PUT` | `/products/{product_id}` | Update a product | Coming soon |
| `DELETE` | `/products/{product_id}` | Delete a product | Implemented |

### Orders

| Method | Endpoint | Description | Status |
|---|---|---|---|
| `POST` | `/orders` | Create a new order | Coming soon |
| `GET` | `/orders` | List all orders | Coming soon |
| `GET` | `/orders/{id}` | Get a single order | Coming soon |

### Example — Create a Product

```bash
curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with USB receiver",
    "category": "Electronics",
    "price": 29.99,
    "stock_quantity": 150,
    "cost_price": 12.50
  }'
```

**Response** (201 Created):

```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "category": "Electronics",
  "price": 29.99,
  "stock_quantity": 150
}
```

> Notice: `cost_price` is **not** in the response. The `ProductResponse` schema intentionally hides internal pricing from API consumers. This is a real-world pattern — you never expose your margins to customers.

---

## Project Phases — Roadmap

### Phase 1 — Foundation (Current)
- Project structure
- FastAPI setup
- SQLite database
- Pydantic schemas
- Product creation endpoint

### Phase 2 — Complete CRUD
- Full Product CRUD (GET, PUT, DELETE)
- Order creation with stock deduction
- Pagination and filtering

### Phase 3 — Error Handling & Middleware
- Custom exceptions (ProductNotFound, OutOfStock)
- Global exception handlers
- Request timing middleware
- Input sanitization

### Phase 4 — Database Evolution
- Migrate from raw `sqlite3` to SQLAlchemy ORM
- Repository pattern (separate DB queries from business logic)
- Alembic for database migrations

### Phase 5 — Authentication & Security
- JWT authentication
- Role-based access control (admin vs customer)
- Rate limiting
- CORS configuration

### Phase 6 — Testing
- Unit tests with pytest
- Integration tests for API endpoints
- Test fixtures and factories

### Phase 7 — AI/RAG Integration
- Product search using embeddings
- Natural language order queries
- RAG-powered customer support

---

## Things I Learned Building This

1. **`CREATE TABLE IF NOT EXISTS` does not update existing tables** — If you change your schema in `database.py` but the table already exists in `ecommerce.db`, SQLite silently ignores the new columns. You have to drop and recreate the table (or use migrations in production).

2. **Pydantic validates before your code runs** — If someone sends `price: -100`, FastAPI returns a `422` error before `create_product()` is ever called. Your controller never sees bad data.

3. **Response schemas hide internal fields** — `ProductCreate` accepts `cost_price`, but `ProductResponse` does not include it. This means API consumers never see your cost data. Same pattern Netflix uses to hide internal metadata.

4. **`__init__.py` makes folders importable** — Without it, `from app.config.settings import ...` would fail. Python needs this file to treat a directory as a package.

5. **`.env` files should never be committed** — Secrets like `ADMIN_API_KEY` belong in `.env`, which is listed in `.gitignore`. In production, these come from environment variables or secret managers.

6. **Uvicorn's `--reload` flag watches for file changes** — Great for development, never use in production. It restarts the server every time you save a file.

---

## Common Interview Questions Based on This Project

### Architecture

1. **Why separate routes from controllers?**
   Routes define *what* endpoints exist. Controllers define *what happens* when those endpoints are hit. This separation means you can reuse controller logic across multiple routes, test business logic without HTTP, and keep each file small and focused.

2. **What is the difference between a schema and a model?**
   In this project, schemas (Pydantic) validate API input/output. Models (database tables) define how data is stored. They often look similar but serve different purposes. A schema might hide `cost_price` from the response while the model stores it.

3. **Why use environment variables instead of hardcoding config?**
   Because the same code runs in development, staging, and production. Each environment has different database paths, API keys, and settings. Environment variables let you change behavior without changing code.

### FastAPI Specific

4. **What does `response_model` do in a route decorator?**
   It tells FastAPI which schema to use when serializing the response. FastAPI will strip any fields not in the response model, validate the output, and document it in Swagger automatically.

5. **What happens if Pydantic validation fails?**
   FastAPI catches the `ValidationError` and returns a `422 Unprocessable Entity` with detailed error messages showing exactly which fields failed and why.

6. **What is `APIRouter` and why use it?**
   `APIRouter` lets you group related endpoints in separate files. Without it, every endpoint would be in `main.py`. With it, products have their own file, orders have their own file, and `main.py` just wires them together.

### Database

7. **Why `CREATE TABLE IF NOT EXISTS` instead of just `CREATE TABLE`?**
   Because the startup function runs every time the app starts. Without `IF NOT EXISTS`, the second startup would crash with "table already exists".

8. **What is `cursor.lastrowid`?**
   After an INSERT, SQLite assigns an auto-incremented ID to the new row. `lastrowid` gives you that ID so you can return it in the response without making another query.

9. **Why close the database connection after each operation?**
   SQLite has limited concurrent connections. If you open connections without closing them, you'll eventually run out and your app will hang. In production with PostgreSQL, you'd use connection pooling instead.

### Security

10. **Why is `cost_price` in `ProductCreate` but not in `ProductResponse`?**
    Because `cost_price` is internal business data. Exposing it would reveal your profit margins. The response schema acts as a security filter — only fields you explicitly include are sent to the client.

---

## License

This project is for learning purposes.
