# `app/controllers/` — Business Logic Layer

> Where the real work happens. Controllers execute database operations, apply business rules, and return structured responses.

## Why Separate Controllers From Routes?

Routes define *what* endpoints exist. Controllers define *what happens* when those endpoints are called. This separation lets you:

- **Reuse logic** — Call `create_product()` from a route, a CLI tool, or a test
- **Test without HTTP** — Unit test business logic directly, no server needed
- **Keep files focused** — Routes stay small, controllers stay testable

## Files

### `product_controller.py`

| Function | Purpose |
|---|---|
| `create_product(product)` | INSERT into database, return `ProductResponse` |
| `get_all_products()` | SELECT all products, return list of `ProductResponse` |
| `get_product_by_id(product_id)` | SELECT by ID, raise `ProductNotFoundException` if missing |
| `delete_product(product_id)` | DELETE by ID, raise `ProductNotFoundException` if missing |

### `order_controller.py`

Placeholder for order business logic (coming in Phase 2).

## How Exception Handling Works

Controllers raise domain exceptions — they never return HTTP status codes directly:

```python
if row is None:
    raise ProductNotFoundException(product_id)
    # Controller says: "I couldn't find this product."
    # It doesn't know about 404, JSON, or HTTP.
```

The global exception handler in `app/exceptions/handlers.py` catches this and translates it into a `404` JSON response.

## Request Flow

```
Route ──► app/controllers/ ──► Database ──► Response
               ▲
          [You are here]
```

## Real-World Analogy

Controllers = **The chef in a restaurant**. The waiter (route) takes the order and brings it to the kitchen. The chef (controller) reads the order, checks the pantry (database), cooks the meal (business logic), and plates it (response schema).

## Best Practices

**Do:** Close `conn.close()` before raising exceptions to prevent connection leaks.

**Don't:** Import `APIRouter` or return `JSONResponse` from controllers. They should know nothing about HTTP.

## 30-Second Revision

- Controllers contain all business logic and database operations
- They are called by route handlers
- They raise custom exceptions for error cases (never HTTP status codes)
- They return Pydantic schema objects (never raw dictionaries for success responses)
- Always close database connections — especially before raising exceptions
