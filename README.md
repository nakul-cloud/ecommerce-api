<div align="center">

# E-Commerce API

**A production-grade REST API built with FastAPI — designed for learning professional backend architecture**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [API Reference](#api-reference) • [Project Structure](#project-structure) • [What I Learned](#what-i-learned)

</div>

---

## Overview

This is not a tutorial project with everything crammed into one file. This is a **properly architected** FastAPI backend that mirrors how production APIs are built at real companies — just scaled down so every design decision is visible and understandable.

The goal: build a backend that I can revisit after a year and understand the architecture within 15 minutes by reading the code and documentation alone.

> [!NOTE]
> This project is actively developed as a phased learning journey. Each phase introduces new backend engineering concepts while keeping the codebase clean and well-documented.

## Features

### Implemented

- **Layered Architecture** — Routes, Controllers, Schemas, and Config cleanly separated
- **Product CRUD** — Create, List, Retrieve, and Delete operations
- **Pydantic Validation** — Strict request/response schemas with field-level constraints
- **Custom Exception Handling** — Domain exceptions with global handlers returning clean JSON errors
- **Environment Configuration** — Secrets loaded from `.env`, never hardcoded
- **Auto-generated API Docs** — Swagger UI and ReDoc available out of the box
- **Database Auto-setup** — Tables created automatically on first startup
- **Request Timing Middleware** — Intercepts requests to log execution duration and adds custom header `X-Process-Time` to response

### Planned

- Product Update operation
- Order management with stock validation
- JWT authentication and role-based access
- Migration from raw SQL to SQLAlchemy + Alembic
- Automated testing with pytest
- AI/RAG integration for product search

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/nakul-cloud/ecommerce-api.git
cd ecommerce-api

# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn python-dotenv
```

### Run

```bash
uvicorn app.main:app --reload
```

The API starts at **http://127.0.0.1:8000**

### Try it

```bash
# Create a product
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

> [!TIP]
> Notice that `cost_price` is **not** in the response. The `ProductResponse` schema intentionally hides internal pricing from API consumers. This is a real-world pattern — you never expose your margins to customers.

## Architecture

### Request Lifecycle

Every API request flows through these layers in order. Each layer has exactly one job.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#2b303c',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#4a5568',
    'lineColor': '#a0aec0',
    'secondaryColor': '#1a202c',
    'tertiaryColor': '#2d3748'
  }
}}%%
flowchart TD
    Client([💻 Client: Browser / Postman / curl])
    
    subgraph FastAPIApp [FastAPI Application Framework]
        Middleware["🛡️ Middleware<br/><i>Intercepts all requests</i><br/>(e.g., Timing & Console Logging)"]
        
        Route["📍 Route Router<br/><i>Matches URL & Method to Handler</i><br/>(e.g., POST /products → create_new_product)"]
        
        Schema{"✔️ Pydantic Schema Validation<br/><i>Validates input formats & rules</i><br/>(e.g., name ≥ 3 chars, price > 0)"}
        
        Controller["⚙️ Controller<br/><i>Executes business logic & DB operations</i><br/>(e.g., create_product() → INSERT)"]
        
        ExcHandler["⚠️ Global Exception Handler<br/><i>Intercepts domain errors & formats responses</i>"]
        
        Response["📦 Response Serialization<br/><i>Filters outgoing database objects</i><br/>(e.g., ProductResponse hides cost_price)"]
    end
    
    %% Request flow
    Client -->|1. HTTP Request| Middleware
    Middleware -->|2. Process Request| Route
    Route -->|3. Route matched| Schema
    
    %% Schema Validation Branching
    Schema -->|✓ Valid input| Controller
    Schema -.->|✗ Invalid: 422 Unprocessable Entity| Client
    
    %% Controller Flow & Errors
    Controller -->|4. Returns raw data| Response
    Controller -.->|✗ Raises custom exception<br/>e.g., ProductNotFoundException| ExcHandler
    
    %% Error translation & Output
    ExcHandler -->|Translates to HTTP 404/400 JSON| Response
    Response -->|5. HTTP Response - Clean JSON| Client

    %% Styles and Colors
    classDef client fill:#3182ce,stroke:#2b6cb0,color:#fff,stroke-width:2px;
    classDef middleware fill:#4a5568,stroke:#2d3748,color:#fff,stroke-width:2px;
    classDef route fill:#805ad5,stroke:#6b46c1,color:#fff,stroke-width:2px;
    classDef schema fill:#d69e2e,stroke:#b7791f,color:#fff,stroke-width:2px;
    classDef controller fill:#319795,stroke:#2c7a7b,color:#fff,stroke-width:2px;
    classDef handler fill:#e53e3e,stroke:#c53030,color:#fff,stroke-width:2px;
    classDef response fill:#38a169,stroke:#2f855a,color:#fff,stroke-width:2px;
    classDef app fill:#f7fafc,stroke:#edf2f7,color:#2d3748,stroke-width:2px,stroke-dasharray: 5 5;

    class Client client;
    class Middleware middleware;
    class Route route;
    class Schema schema;
    class Controller controller;
    class ExcHandler handler;
    class Response response;
    class FastAPIApp app;
```

### Design Decisions

| Decision | Why |
|---|---|
| **Separate routes from controllers** | Routes define *what* endpoints exist. Controllers define *what happens*. This makes business logic reusable and testable without HTTP. |
| **Input schema ≠ Response schema** | `ProductCreate` accepts `cost_price`. `ProductResponse` hides it. The API never exposes internal data. |
| **Custom exceptions over HTTP exceptions** | Controllers raise `ProductNotFoundException` — they don't know about HTTP status codes. The global handler translates it to `404`. Clean separation. |
| **`CREATE TABLE IF NOT EXISTS`** | Startup runs every time. Without `IF NOT EXISTS`, the second startup would crash. |
| **`.env` for configuration** | Same code runs in dev, staging, and production. Only the `.env` file changes. |

## API Reference

### Interactive Documentation

| URL | Description |
|---|---|
| http://127.0.0.1:8000/docs | **Swagger UI** — interactive, test endpoints directly |
| http://127.0.0.1:8000/redoc | **ReDoc** — clean read-only documentation |

### Endpoints

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/` | Health check | `200` |
| `POST` | `/products` | Create a new product | `201` |
| `GET` | `/products` | List all products | `200` |
| `GET` | `/products/{product_id}` | Retrieve a single product | `200` |
| `DELETE` | `/products/{product_id}` | Delete a product | `200` |

### Error Responses

When something goes wrong, the API returns structured JSON errors:

```json
{
  "status": "error",
  "message": "Product with ID 99 not found"
}
```

| Status Code | When |
|---|---|
| `404` | Product not found |
| `422` | Validation failed (missing fields, invalid types, constraints violated) |
| `500` | Unexpected server error |

## Project Structure

```
ecommerce-api/
├── app/                          # Application package
│   ├── main.py                   # FastAPI app, startup, router wiring
│   ├── config/
│   │   ├── settings.py           # Environment variables (.env loader)
│   │   └── database.py           # SQLite connection + table creation
│   ├── routes/
│   │   ├── products.py           # /products endpoint definitions
│   │   └── orders.py             # /orders (placeholder)
│   ├── controllers/
│   │   ├── product_controller.py # Product business logic + DB operations
│   │   └── order_controller.py   # Order logic (placeholder)
│   ├── schemas/
│   │   ├── product_schema.py     # ProductCreate, ProductUpdate, ProductResponse
│   │   └── order_schema.py       # OrderItem, OrderCreate, OrderResponse
│   ├── exceptions/
│   │   ├── custom_exceptions.py  # ProductNotFoundException
│   │   └── handlers.py           # Global exception → JSON response mapping
│   ├── middleware/
│   │   └── timing.py             # Request duration logging middleware
│   └── utils/
│       ├── constants.py          # App-wide constants (placeholder)
│       └── helpers.py            # Reusable helper functions (placeholder)
├── data/
│   └── ecommerce.db              # SQLite database (auto-created)
├── tests/                        # Test suite (coming soon)
├── .env                          # Environment secrets (not committed)
├── .gitignore                    # Git ignore rules
└── requirements.txt              # Python dependencies
```

> [!IMPORTANT]
> Every folder contains its own `README.md` with detailed explanations of purpose, responsibilities, request flow, best practices, and interview questions. Navigate into any folder to learn more.

## Tech Stack

| Technology | Role | Why This Choice |
|---|---|---|
| **Python 3.11+** | Language | Industry standard for backend + AI/ML |
| **FastAPI** | Web framework | Auto-validation, auto-docs, async-ready, type hints |
| **Uvicorn** | ASGI server | Runs FastAPI applications |
| **SQLite** | Database | Zero-config, file-based — perfect for learning, swap to PostgreSQL later |
| **Pydantic** | Validation | Catches bad input before your code runs |
| **python-dotenv** | Configuration | Loads secrets from `.env` so they never touch source code |

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| **Phase 1** | Project structure, FastAPI setup, SQLite, Product CRUD, Schemas, Exceptions | **Done** |
| **Phase 2** | Product Update, Order CRUD with stock deduction, Pagination | Planned |
| **Phase 3** | Request timing middleware (Done), Input sanitization | In Progress |
| **Phase 4** | SQLAlchemy ORM, Repository pattern, Alembic migrations | Planned |
| **Phase 5** | JWT authentication, Role-based access, Rate limiting | Planned |
| **Phase 6** | Automated testing with pytest, Test fixtures | Planned |
| **Phase 7** | AI/RAG integration — product search with embeddings | Planned |

## What I Learned

Building this project taught me patterns that tutorials rarely cover:

1. **`CREATE TABLE IF NOT EXISTS` does not update existing tables.** If you add a column to your schema definition but the table already exists in SQLite, the change is silently ignored. You must drop and recreate (or use migrations in production).

2. **Pydantic validates before your code runs.** If someone sends `price: -100`, FastAPI returns `422` before `create_product()` is ever called. Your business logic never sees bad data.

3. **Response schemas are security filters.** `ProductCreate` accepts `cost_price`, but `ProductResponse` excludes it. API consumers never see your cost data.

4. **Controllers should not know about HTTP.** A controller raises `ProductNotFoundException`. It has no idea that this becomes a `404` response. The exception handler does that translation. This is real separation of concerns.

5. **Always close database connections before raising exceptions.** Forgetting `conn.close()` before `raise` leaks connections. SQLite has limited concurrency — leaked connections cause the app to hang.

6. **`__init__.py` makes folders importable.** Without it, `from app.config.settings import ...` throws `ModuleNotFoundError`. It looks empty but it's essential.

## Troubleshooting

### `sqlite3.OperationalError: table has no column named X`

The table was created with an older schema. `CREATE TABLE IF NOT EXISTS` won't update it.

**Fix:** Delete `data/ecommerce.db` and restart the server. Tables will be recreated with the current schema.

### `ModuleNotFoundError: No module named 'dotenv'`

Dependencies are not installed in your virtual environment.

**Fix:** Activate your `.venv` and run `pip install python-dotenv`.

### `UnicodeEncodeError` on Windows terminal

Windows console may not support Unicode characters (like emojis) in print statements.

**Fix:** Avoid emoji characters in `print()` statements, or set `PYTHONIOENCODING=utf-8`.
