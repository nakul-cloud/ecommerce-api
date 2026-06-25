# `app/routes/` — API Endpoint Definitions

> Maps HTTP requests to controller functions. Routes define *what* endpoints exist — controllers define *what happens*.

## Files

### `products.py`

Defines all `/products` endpoints using FastAPI's `APIRouter`.

| Method | Path | Handler | Status Code | Description |
|---|---|---|---|---|
| `POST` | `/products` | `create_new_product()` | `201` | Create a new product |
| `GET` | `/products` | `get_products()` | `200` | List all products |
| `GET` | `/products/{product_id}` | `get_product()` | `200` | Retrieve a single product |
| `DELETE` | `/products/{product_id}` | `del_product()` | `200` | Delete a product |

### `orders.py`

Placeholder for `/orders` endpoints (coming in Phase 2).

## How Routes Work

```python
# This is all a route does:
@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(product: ProductCreate):
    return create_product(product)    # ← delegates to controller
```

The route function is 1 line. It receives validated input (Pydantic handles that), calls the controller, and returns the result. Zero business logic.

## Request Flow

```
Client ──► app/routes/ ──► Controller ──► Database ──► Response
              ▲
         [You are here]
```

## Real-World Analogy

Routes = **Reception desk**. They look at what the visitor wants, verify their paperwork (schemas), and direct them to the right manager (controller). They don't do the work themselves.

## Best Practices

**Do:** Define a clear `prefix` and `tags` for each router. Always specify `response_model` to filter the response.

**Don't:** Write database queries or business logic inside route files.

## 30-Second Revision

- `routes/` maps HTTP methods + paths to Python handler functions
- `APIRouter` groups endpoints by feature domain
- `response_model` controls which fields appear in the response (security filter)
- Route functions should contain zero business logic — only delegation
