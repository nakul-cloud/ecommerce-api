# `app/exceptions/` — Error Handling Layer

This folder houses application-specific exception classes and global handlers to ensure that error messages are handled uniformly, securely, and cleanly.

---

## 1. Purpose

> Why do we have an exceptions folder?

In professional API development, controllers should only focus on business logic. If a business validation fails (e.g. a product isn't found), the controller should immediately stop execution and declare the issue by raising an exception, without worrying about HTTP protocols, JSON formats, or status codes. 

The `exceptions/` folder separates:
- **What went wrong** (defined by Custom Exceptions)
- **How to respond to the client** (defined by Global Exception Handlers)

This division ensures that:
- **Tracebacks are hidden**: Raw Python or database error stack traces never leak to API consumers.
- **API responses are uniform**: Error schemas remain standardized (e.g. `{"status": "error", "message": "..."}`).
- **Controllers stay clean**: Zero HTTP or JSON serialization logic inside the database query routines.

---

## 2. Responsibilities

### What belongs inside `exceptions/`

- Custom exception classes subclassing Python's base `Exception` class.
- Global exception handler registration logic mapping custom exceptions to FastAPI's response cycle.

### What does NOT belong inside `exceptions/`

- Business calculations or database CRUD scripts.
- Router endpoint path decorators.

---

## 3. Files

### `custom_exceptions.py`

- **Purpose**: Defines custom domain exception classes representing business/domain problems.
- **Classes**:
  - `ProductNotFoundException`: Raised when a requested product ID does not exist in the database.
  - `ProductOutOfStockException`: Raised when a product is requested with a quantity exceeding its database stock level.
  - `OrderNotFoundException`: Raised when a requested order ID does not exist in the database.
  - `InvalidCredentialsException`: Raised when user login email or password verification fails.
  - `InvalidTokenException`: Raised when a JWT token signature verification fails, is missing, or is expired.
  - `PermissionDeniedException`: Raised when the current user's role is not authorized to access a route (e.g. customer accessing admin routes).
- **Who calls it**: Raised inside controllers like `product_controller.py`, `order_controller.py`, `user_controller.py`, and `auth_controller.py`.

### `handlers.py`

- **Purpose**: Defines how FastAPI should translate custom exceptions into HTTP JSON responses.
- **Functions**:
  - `register_exception_handlers(app: FastAPI)`: Hooks all custom exception handlers to the FastAPI app instance on startup. Registers handlers mapping:
    - `ProductNotFoundException` &rarr; `404 Not Found`
    - `ProductOutOfStockException` &rarr; `409 Conflict`
    - `OrderNotFoundException` &rarr; `404 Not Found`
    - `InvalidCredentialsException` &rarr; `401 Unauthorized`
    - `InvalidTokenException` &rarr; `401 Unauthorized`
    - `PermissionDeniedException` &rarr; `403 Forbidden`
- **Who calls it**: Registered in `app/main.py`.

---

## 4. Request Flow & Exception Lifecycle

When a request triggers an error, execution stops immediately and bubbles up to the global handler:

```
    [Controller]
         │  
         │ (if row is None)
         ▼
  ProductNotFoundException (Raised!)
         │
         ▼ (Interrupts normal request execution)
  [Global Exception Handler]
         │
         ▼ (Formats into clean JSON response)
  404 Not Found + JSON Response
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

Custom exceptions describe **what** went wrong in your application's logic (like `ProductNotFoundException`), while exception handlers decide **how** the API should respond back to the user (like returning a `404` status code with a clean error message). This keeps business code clean: the controller throws the red flag, and the handler decides how to clean up the mess.

---

## 6. Real-World Analogy

Imagine a hospital:

1. **Doctor (Controller)**: Diagnoses the problem: *"The patient has a broken arm."*
2. **Diagnosis (Custom Exception)**: `"BrokenArmException"`
3. **Reception/Billing (Global Exception Handler)**: Decides what paperwork, room assignment, and insurance billing process should follow.

The doctor doesn't handle billing, and the receptionist doesn't diagnose injuries.

The same separation applies here:
- **Controller** → Identifies the application problem.
- **Custom Exception** → Names that problem.
- **Global Exception Handler** → Converts it into a proper API response.

---

## 7. Custom Exceptions vs. Global Handlers

| Custom Exception | Global Exception Handler |
|---|---|
| Defines **what** went wrong | Defines **how to respond** to the client |
| Business/Domain logic level | HTTP/API protocol level |
| Raised by controllers | Registered in FastAPI application |
| Example: `ProductNotFoundException` | Returns `404 Not Found` JSON response |
| Example: `ProductOutOfStockException` | Returns `409 Conflict` JSON response |
| Example: `OrderNotFoundException` | Returns `404 Not Found` JSON response |
| Example: `InvalidCredentialsException` | Returns `401 Unauthorized` JSON response |
| Example: `InvalidTokenException` | Returns `401 Unauthorized` JSON response |
| Example: `PermissionDeniedException` | Returns `403 Forbidden` JSON response |

### What about technical errors?
System/Technical errors are different from business exceptions (e.g. SQLite connection failed, database timeouts, network errors, or division-by-zero). We can handle these globally using a general catch-all handler:
```python
@app.exception_handler(Exception)
```
This intercepts unexpected bugs, logs the real traceback on the server console for developers, and returns a safe, generic message to the client:
```json
{
    "status": "error",
    "message": "Internal Server Error"
}
```

---

## 8. Best Practices

### Do

- Inherit custom exceptions from Python's base `Exception` class.
- Always close database resources (`conn.close()`) in your controller *before* raising exceptions.
- Provide descriptive error messages inside exceptions so the handler can read `exc.message` directly.

### Don't

- Avoid putting HTTP status codes directly inside custom exception definitions to preserve logic separation.
- Never let raw SQL strings or driver tracebacks leak in exception responses.

---

## 9. Interview Questions

1. **Why separate custom exceptions from global exception handlers?**
   To decouple business logic from HTTP protocols. Controllers shouldn't care about JSON formats or status codes; they only care about whether their business operations succeeded.
2. **What happens if an unhandled exception occurs inside a route?**
   FastAPI's default error handler catches it, logs the traceback, and returns a general `500 Internal Server Error` response to the client.
3. **How does Python's `super().__init__(self.message)` work in exceptions?**
   It initializes the base `Exception` class with the custom error message string, making it retrievable via `str(exc)`.

---

## 10. Quick Revision

### 30-Second Revision

- **Custom Exceptions** declare *what* went wrong in application logic (e.g., `ProductNotFoundException`).
- **Global Handlers** translate those exceptions into HTTP JSON responses (e.g., `404 Not Found`).
- **Separation of Concerns**: Controllers raise errors; Handlers format responses.
- **Technical Exceptions** (like database connection issues) are caught globally to hide stack traces and return clean `500` status codes.
- **Resource Management**: Always release database connections before raising exceptions.
- Exception handlers are registered globally on the `FastAPI` instance at startup in `main.py`.
