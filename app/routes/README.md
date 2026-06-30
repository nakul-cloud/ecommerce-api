# `app/routes/` — API Endpoint Definitions & Routing Layer

> Maps incoming HTTP requests to their corresponding controller functions, enforces security guards via dependencies, and formats output schemas.

---

## 1. Overview & Purpose

In clean web architecture, the **Routing Layer** acts as the external gateway of the application. Its responsibility is strictly limited to mapping HTTP methods (GET, POST, DELETE, etc.) and URL paths to executable Python code. 

### Why keep routes separate and lightweight?
1. **Zero Business Logic**: Routes should only delegate. If you write SQL or calculations inside a route handler, you mix transport protocols (HTTP) with business rules.
2. **Centralized Version Prefixing**: Routes are registered under `api_v1_router` in `main.py` using a single route aggregator at [index.py](file:///d:/ecommerce-api/app/routes/index.py). All endpoints are prefixed with `/api/v1`.
3. **Guardhouse Security**: Endpoint access rules (authentication and role checks) are declared directly on the route using FastAPI's dependency injection system (`Depends`), keeping controllers clean.
4. **Thin Route Decorators**: Because the controllers return standardized envelopes (via `JSONResponse`), status codes and output formats are configured in the controllers. Route decorators do not specify redundant `status_code` or `response_model` values.

---

## 2. Request Flow & Middleware Gateway

When a request reaches the application, the Routing Layer processes input validation and authorization checks before calling the controller:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#f8fafc', 'primaryTextColor': '#1e293b', 'primaryBorderColor': '#cbd5e1', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'nodeTextColor': '#e9ff89ff', 'textColor': '#1e293b', 'titleColor': '#ffffff', 'edgeLabelBackground': '#ffffff', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#cbd5e1', 'actorBkg': '#f8fafc', 'actorBorder': '#cbd5e1', 'actorTextColor': '#1e293b', 'signalColor': '#4f46e5', 'signalTextColor': '#ffffff', 'noteBkgColor': '#fef08a', 'noteBorderColor': '#facc15', 'noteTextColor': '#713f12'}}}%%
flowchart LR
    Client([Client]) -->|1. HTTP Request| Router[APIRouter]
    Router -->|2. Enforce Security| Auth{Depends Auth}
    Auth -->|Fail: 401/403| Client
    Auth -->|Pass| Schema[Pydantic Validate]
    Schema -->|Fail: 422| Client
    Schema -->|Pass| Controller[Controller Class staticmethod]
    Controller -->|3. Business Logic / DB| DB[(SQLite DB)]
    DB -->|4. Return Data| Controller
    Controller -->|5. Format response_envelope| Router
    Router -->|6. JSON Response| Client
    
    style Router fill:#4f46e5,stroke:#3730a3,color:#ffffff
    style Auth fill:#f59e0b,stroke:#d97706,color:#ffffff
```

---

## 3. Route Specifications & Endpoints

All route files are grouped by domain and invoke class-based controllers:

*   **Auth Routes (`auth_routes.py`)**: Routes prefixed with `/auth`. Maps to static methods on `AuthController`.
*   **User Routes (`user_routes.py`)**: Routes prefixed with `/users`. Maps to static methods on `UserController`.
*   **Product Routes (`product_routes.py`)**: Routes prefixed with `/products`. Maps to static methods on `ProductController`.
*   **Order Routes (`order_routes.py`)**: Routes prefixed with `/orders`. Maps to static methods on `OrderController`.

---

## 4. Key Patterns: FastAPI Dependency Injection

FastAPI's dependency injection system (`Depends`) executes pre-requisite functions prior to invoking our route handlers. For example:

```python
@router.post("")
def store(
    product: ProductCreate,
    current_user: UserResponse = Depends(require_role(ADMIN))
):
    return ProductController.store(product)
```

1. **Extraction**: FastAPI identifies `Depends(require_role(ADMIN))`.
2. **Chain Resolution**: `require_role` returns a helper dependency that demands `Depends(get_current_user)`.
3. **Execution**: FastAPI extracts the Bearer token from the `Authorization` header, decodes and validates the JWT, checks if the user exists and is active in the database.
4. **Authorization check**: The role checker asserts `current_user.role in (ADMIN,)`. If false, it raises a `PermissionDeniedException` (which bubbles up to trigger a `403 Forbidden` response).
5. **Route execution**: Only if all checks pass does FastAPI invoke the controller static method `ProductController.store(product)`.

---

## 5. Real-World Analogy

Think of routes as the **Hospital Wards Reception Desks**:
- **Public Wards (GET /products)**: Anyone can walk in and read the information boards. No security check required.
- **Patient Registration desk (POST /users/register)**: Open to the public, but you must fill out the correct intake form (Pydantic schema).
- **Intensive Care Unit (POST /orders)**: Locked ward. You must present a valid staff/patient wristband (JWT Bearer Token) at the entrance checkpoint (`Depends(get_current_user)`).
- **Medicine Vault (POST /products)**: Only doctors with high-security badges can access. You must present your wristband showing you have the administrative clearance rank (`Depends(require_role(ADMIN))`).

---

## 6. Interview Questions & Design Takeaways

### 1. What is the difference between Path parameters and Query parameters?
* **Path Parameters** (e.g. `/products/{product_id}`): Used to identify a *specific resource* in the database hierarchy. They are mandatory parts of the URL.
* **Query Parameters** (e.g. `/products?category=electronics&limit=10`): Used to *filter, sort, or paginate* lists of resources. They are optional modifiers appended after the `?`.

### 2. Why shouldn't you put database connections or SQL queries in the route file?
Coupling database drivers and query logic directly in route files violates the **Single Responsibility Principle**. If you ever decide to change your database layer (e.g. migration from raw SQL to an ORM like SQLAlchemy), you would have to modify all your route files. Keeping SQL inside services isolates transport protocols (HTTP) from data persistence.

---

## 7. 30-Second Revision

- **Routing Layer** maps requests (URL + Method) to controller handlers.
- **Aggregated Routing** registers all routes under the versioned prefix `/api/v1`.
- **Thin Decorators** declare the path and endpoint wrapper dependencies.
- **Dependencies** (`Depends`) act as reusable pre-execution security guards.
- **Route handlers** are clean, single-line wrappers that delegate immediately.
