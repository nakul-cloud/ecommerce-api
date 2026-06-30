<div align="center">

# E-Commerce API

**A production-grade REST API built with FastAPI — designed for learning professional backend architecture**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)

<br/>

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [API Reference](#api-reference) • [Project Structure](#project-structure) • [What I Learned](#what-i-learned)

</div>

---

<br/>

## Overview

This is not a tutorial project with everything crammed into one file. This is a **properly architected** FastAPI backend that mirrors how production APIs are built at real companies — just scaled down so every design decision is visible and understandable.

The goal: build a backend that I can revisit after a year and understand the architecture within 15 minutes by reading the code and documentation alone.

<br/>

> [!NOTE]
> This project is actively developed as a phased learning journey. Each phase introduces new backend engineering concepts while keeping the codebase clean and well-documented.

<br/>

---

<br/>

## Features

### Implemented

* **Layered Architecture** — Routes, Class-based Controllers, Business Services, and Config cleanly separated.
* **Product CRUD** — Create, List, Retrieve, and Delete operations.
* **Order CRUD** — Create orders, list all orders, and retrieve a single order by ID with inventory stock deduction.
* **User & Admin Registration** — Customer sign-up and secure administrator registration guarded by a registration key.
* **JWT Stateless Authentication** — Token generation/decoding using **`PyJWT`** with secure password hashing using `passlib` (bcrypt). Conforms with OAuth2 specifications allowing native Swagger UI "Authorize" token parsing.
* **Role-Based Access Control (RBAC)** — Reusable route dependencies enforce customer or admin permissions (`Depends(require_role("admin"))`), supporting multiple roles checker using varargs (`*roles: str`).
* **Pydantic Validation & Sanitization** — Strict request/response schemas with field-level constraints. Includes automatic data cleansing (whitespace trimming and email lowercasing) using Pydantic `@field_validator` hooks.
* **Internal Schemas** — `ValidatedOrderItem` separates controller-internal data from public API schemas.
* **Unified Exception Handling** — Custom exceptions (like `ProductNotFoundException`, `ProductOutOfStockException`) mapped to a base `AppException` which is caught globally to return consistent JSON error envelopes.
* **Modular Middleware Pipeline** — Restructured middlewares: Timing middleware, security headers (using `secure`), IP-based rate limiting (using `slowapi`), GZip compression, and CORS.
* **Environment Configuration** — Settings configuration parameters parsed and validated via `pydantic-settings` from `.env`.
* **Standard Logging System** — Logging utility in `logger.py` replacing raw `print()` calls, redirecting outputs both to the console and to a persistent log file (`logs/app.log`).
* **Auto-generated API Docs** — Swagger UI and ReDoc available out of the box (with secure headers bypassed specifically for documentation endpoints).
* **Database Auto-setup** — Tables created automatically on startup inside the modern ASGI `lifespan` hook.
* **Database Seeder** — Command (`python -m app.seed.seed_database`) populates 1 admin + 100 customers + 250 products + 1000 orders using `Faker`.

<br/>

### Planned

* Product Update operation and pagination
* Migration from raw SQLite to PostgreSQL with SQLAlchemy + Alembic
* Automated testing with pytest
* AI/RAG integration for product search

<br/>

---

<br/>

## Quick Start

### Prerequisites

* Python 3.11 or higher
* Git

<br/>

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
pip install fastapi uvicorn pydantic-settings slowapi secure pyjwt passlib bcrypt faker httpx
```

<br/>

### Run

```bash
uvicorn app.main:app --reload
```

The API starts at **http://127.0.0.1:8000**

<br/>

### Seed Demo Data (Optional)

Populate the database with realistic demo data in one command:

```bash
python -m app.seed.seed_database
```

This creates **1 admin + 100 customers + 250 products + 1000 orders**.

**Default admin login:** `admin@example.com` / `admin123`

<br/>

### Try it

```bash
# Create a product (after authorizing in Swagger UI)
curl -X POST http://127.0.0.1:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
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
  "status": "success",
  "message": "Product created successfully.",
  "data": {
    "id": 1,
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with USB receiver",
    "category": "Electronics",
    "price": 29.99,
    "stock_quantity": 150
  }
}
```

<br/>

> [!TIP]
> Notice that `cost_price` is **not** in the response. The `ProductResponse` schema intentionally hides internal pricing from API consumers. This is a real-world pattern — you never expose your margins to customers.

<br/>

---

<br/>

## Architecture

### Request Lifecycle

Every API request flows through these layers in order. Each layer has exactly one job.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'nodeTextColor': '#1e293b', 'textColor': '#ffffff', 'titleColor': '#ffffff', 'edgeLabelBackground': '#1e293b', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#e2e8f0', 'actorBkg': '#f8fafc', 'actorBorder': '#cbd5e1', 'actorTextColor': '#1e293b', 'signalColor': '#4f46e5', 'signalTextColor': '#ffffff', 'noteBkgColor': '#fef08a', 'noteBorderColor': '#facc15', 'noteTextColor': '#713f12'}}}%%
sequenceDiagram
    autonumber
    actor Client
    participant Middleware as Middleware (Interceptors)
    participant Route as Route Layer (APIRouter)
    participant Schema as Schema Layer (Pydantic)
    participant Controller as Controller Layer (Orchestration)
    participant Service as Service Layer (Business Logic)
    participant DB as Database (SQLite)

    Client->{}+Middleware: HTTP Request
    Note over Middleware: Records timing start_time / checks rate limit
    
    Middleware->>Route: Forward Request
    
    Route->>Schema: Validate & Sanitize Input
    alt Validation Fails
        Schema-->>Client: HTTP 422 (Unprocessable Content)
    else Validation Succeeds
        Schema-->>Route: Valid Data Object
        
        Route->>Controller: Call Controller staticmethod
        
        Controller->>Service: Invoke Business Service
        activate Service
        
        Service->>DB: Query / Connect / Transaction
        activate DB
        DB-->>Service: SQL Rows / Result
        deactivate DB
        
        alt Out of Stock / Entity Missing
            Service-->>Controller: Raise Custom Exception (AppException)
            Note over Route: Caught by Global Exception Handler
            Route-->>Client: Return consistent Fail JSON response
        else Success
            Service-->>Controller: Return Domain Model
            deactivate Service
            
            Controller-->>Route: Wrap success_response JSONResponse
            
            Route->>Middleware: Forward Response
            
            Note over Middleware: Adds X-Process-Time / attaches Secure headers
            Middleware-->>Client: HTTP Response (JSONResponse)
            deactivate Client
        end
    end
```

<br/>

### Design Decisions

| Decision | Why |
|---|---|
| **Separating Services from Controllers** | Services isolate SQL statements and database transactions. Controllers coordinate request routing and envelope formatting. |
| **Pydantic validators for sanitization** | Strips strings and normalizes emails automatically at the entry door of schemas, protecting databases from contaminants. |
| **Stateless PyJWT token handler** | Encrypts session identifiers on login using HS256 signatures, avoiding server-side session stores. |
| **Modular Middleware Files** | Separates CORS, rate-limiting, and security headers configurations into modular hooks, keeping `main.py` clean. |
| **Unified exception handling** | Custom domain errors inherit from a base `AppException`, allowing a single global handler to format all responses consistently. |

<br/>

---

<br/>

## API Reference

### Interactive Documentation

| URL | Description |
|---|---|
| http://127.0.0.1:8000/docs | **Swagger UI** — interactive, test endpoints directly |
| http://127.0.0.1:8000/redoc | **ReDoc** — clean read-only documentation |

<br/>

### Authentication

Protected routes require a Bearer token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer <your-jwt-token>" ...
```

You can obtain the JWT access token by sending a POST request to `/api/v1/auth/login` with your credentials (`username` as email, `password`).

---

## Project Structure

Navigate to any sub-directory link below to view its specific, in-depth documentation detailing module flows, design decisions, and common interview questions.

```
ecommerce-api/
├── app/                          # Application package (Core Code)
│   ├── main.py                   # FastAPI app, lifespan setup, router mount
│   ├── config/                   # Configuration settings & DB connections
│   ├── auth/                     # JWT Authentication & authorization guards
│   ├── routes/                   # Thin API Route endpoints & HTTP validation
│   ├── controllers/              # Static class orchestrator controllers
│   ├── services/                 # Database queries & transactions logic
│   ├── schemas/                  # Pydantic input/output schemas
│   ├── exceptions/               # Domain-specific exceptions & handlers
│   ├── middleware/               # HTTP timing, CORS, and security interceptors
│   ├── seed/                     # DB seeder: 100 users, 250 products, 1000 orders
│   └── utils/                    # Shared helper functions (PyJWT, logger, etc.)
├── data/                         # SQLite binary database files
└── tests/                        # Automated unit & integration tests
```

### Module Documentation Directory

* 📂 **Core Application Setup** — [`app/README.md`](file:///d:/ecommerce-api/app/README.md)
* 📂 **Configuration & Database Connections** — [`app/config/README.md`](file:///d:/ecommerce-api/app/config/README.md)
* 📂 **Authentication, JWT & Authorization Guards** — [`app/auth/README.md`](file:///d:/ecommerce-api/app/auth/README.md)
* 📂 **API Route Descriptors & Path Resolvers** — [`app/routes/README.md`](file:///d:/ecommerce-api/app/routes/README.md)
* 📂 **Business Controllers & HTTP Mapping** — [`app/controllers/README.md`](file:///d:/ecommerce-api/app/controllers/README.md)
* 📂 **Core Database & Service Operations** — [`app/services/README.md`](file:///d:/ecommerce-api/app/services/README.md)
* 📂 **Pydantic Validation & Output Formatting Schemas** — [`app/schemas/README.md`](file:///d:/ecommerce-api/app/schemas/README.md)
* 📂 **Custom Exceptions & Global Handlers** — [`app/exceptions/README.md`](file:///d:/ecommerce-api/app/exceptions/README.md)
* 📂 **Timing, Security & Logger Middleware** — [`app/middleware/README.md`](file:///d:/ecommerce-api/app/middleware/README.md)
* 📂 **Database Seeder** — [`app/seed/README.md`](file:///d:/ecommerce-api/app/seed/README.md)
* 📂 **Database Storage Files** — [`data/README.md`](file:///d:/ecommerce-api/data/README.md)
* 📂 **Automated Test Suites** — [`tests/README.md`](file:///d:/ecommerce-api/tests/README.md)
