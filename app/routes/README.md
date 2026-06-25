# `app/routes/` — API Endpoints (Routing Layer)

This folder defines all client-facing URL paths, HTTP methods, and associates them with corresponding controllers.

---

## 1. Purpose

> Why do we have a routes folder?

The routing layer maps HTTP requests to the correct controller functions.
- **Deconstruct URL requests**: Route requests based on HTTP actions (`GET`, `POST`, `PUT`, `DELETE`).
- **Encapsulate schema rules**: Map specific Pydantic schemas to validate requests before execution and filter response bodies before sending them back.
- **Support modular API development**: Break a massive API down into modular sections using FastAPI's `APIRouter`.

Separating routes from business logic makes the code more testable and prevents routing endpoints from becoming bloated.

---

## 2. Responsibilities

### What belongs inside `routes/`

- Route decorators (`@router.get`, `@router.post`).
- Response models definitions (`response_model=ProductResponse`).
- API tags and prefixes for Swagger documentation.
- Delegation of requests directly to controller functions.

### What does NOT belong inside `routes/`

- Database connection queries.
- Business logic or calculations.
- Data mapping.

---

## 3. Files

### `products.py`

- **Purpose**: Defines `/products` endpoints.
- **Endpoints**:
  - `POST /products`: Creates a new product.
  - `GET /products`: Retrieves all products.
  - `GET /products/{product_id}`: Retrieves a single product by its ID.
  - `DELETE /products/{product_id}`: Deletes a product by its ID.
- **When is it called**: When a client sends an HTTP request matching `/products`.
- **Who calls it**: FastAPI's internal routing engine when requests arrive.

### `orders.py`

- **Purpose**: Grouping endpoints for `/orders` (like order creation).
- **When is it called**: When a client requests `/orders`.

---

## 4. Request Flow

The routing layer is the entry point for all incoming API calls matching registered paths:

```
Client (HTTP Request) 
        │
        ▼
 ┌──────────────┐
 │  app/routes  │  ◄── [Routing Layer]
 └──────┬───────┘
        │
        ▼
   Controllers ──► Database ──► Response
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

Routes are like the receptionist at a business office. They sit at the front desk, look at what the visitor wants (e.g. "I want to create a product"), verify their paperwork (schemas), and direct them to the correct manager (controller). They don't do the actual work; they just direct traffic.

---

## 6. Real-World Analogy

- **Routes** = The receptionist or concierge desk.
- **Path Prefix** = The floor numbers (e.g., Floor 3 = `/products`).
- **HTTP Methods** = The action requested (e.g., Deliver package = `POST`, Ask question = `GET`).

---

## 7. Best Practices

### Do

- Define a clean prefix for each router (e.g., `prefix='/products'`).
- Always specify `response_model` to sanitize output and keep secrets safe.
- Define tags to make Swagger UI clean.

### Don't

- Write direct database queries inside route files.
- Put complex business rules inside routing functions.

---

## 8. Interview Questions

1. **Why use FastAPI's `APIRouter`?**
   It allows modularizing the application, making it clean to separate route configurations into different files instead of piling them into a single file.
2. **What does `status_code=status.HTTP_201_CREATED` do?**
   Sets the HTTP response status to `201` (Created), indicating a resource was successfully saved in the database.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Handing inputs directly to controller functions.
- Simple synchronous endpoint definitions.

### Future Evolution
- **Phase 5**: Inject security/authentication dependencies (`Depends(get_current_user)`).

---

## 10. Quick Revision

- `routes/` maps paths and HTTP methods to Python handlers.
- `APIRouter` isolates logic by feature domain.
- Routes validate incoming request bodies automatically using Pydantic schemas.
- `response_model` defines the outgoing structure, filtering private database fields.
- Routes should contain zero business logic; they only delegate.
