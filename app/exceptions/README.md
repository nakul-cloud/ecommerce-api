# `app/exceptions/` — Error Handling Layer

This folder houses application-specific exception classes and handlers to ensure error messages are returned uniformly and cleanly.

---

## 1. Purpose

> Why do we have an exceptions folder?

In professional API development:
- **Avoid raw tracebacks**: Prevent raw backend errors or stack traces from reaching clients.
- **Provide clear, uniform errors**: Standardize error schemas (e.g. `{ "detail": "Product with ID 10 not found" }`).
- **Simplify controller logic**: Let controllers raise exceptions directly (e.g., `raise ProductNotFoundError`) without worrying about writing HTTP response handlers.

---

## 2. Responsibilities

### What belongs inside `exceptions/`

- Custom Exception classes extending Python's base `Exception` or FastAPI's `HTTPException`.
- FastAPI Exception handlers to intercept raised exceptions and transform them into JSON responses.

### What does NOT belong inside `exceptions/`

- Business calculations or routing paths.

---

## 3. Files

### `custom_exceptions.py`

- **Purpose**: Defines custom domain exception classes (e.g., `ProductNotFoundException`, `InsufficientStockException`).
- **When is it called**: Raised by controllers or validators when business operations fail.
- **Who calls it**: Controllers.

### `handlers.py`

- **Purpose**: Wires custom exceptions to FastAPI handlers to format output responses.
- **When is it called**: When a registered custom exception is raised during request execution.
- **Who calls it**: FastAPI's error middleware.

---

## 4. Request Flow

The exceptions layer intercepts raised errors and stops standard execution flow:

```
Client ──► Route ──► Controller (Exception raised!)
                         │
                         ▼ (Intercepted by handlers.py)
Client ◄── JSON Response (404 / 400 with clean error detail)
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

This folder is the customer support desk. If something goes wrong during a request (like ordering a product that doesn't exist), the controller doesn't crash the server. Instead, it raises an exception flag, and the exception handler intercepts it, translates it into a polite, structured message, and sends it back to the client.

---

## 6. Real-World Analogy

- **Exceptions** = Emergency protocols and customer support workers.

---

## 7. Best Practices

### Do

- Keep custom exceptions specific and meaningful.
- Use appropriate HTTP status codes (e.g., 404 for Not Found, 400 for Bad Request).

### Don't

- Never allow raw internal database/system stack trace files to leak to the client.

---

## 8. Interview Questions

1. **Why use custom exceptions instead of returning error dicts?**
   It allows you to break execution flows immediately without nesting logic in controllers, and lets the framework format responses globally.
2. **How do you register an exception handler in FastAPI?**
   Using the `@app.exception_handler(ExceptionClass)` decorator on the FastAPI app instance.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Placeholders created for future execution.

### Future Evolution
- **Phase 3**: Custom `HTTPException` decorators and middleware loggers for auditing application errors.

---

## 10. Quick Revision

- `exceptions/` manages error-handling workflows.
- `custom_exceptions.py` defines business-level exceptions.
- `handlers.py` transforms exceptions into structured HTTP JSON responses.
- Prevents database leaks and raw python trackback errors.
