# `tests/` — Automated Test Suite

> Automated tests to verify API correctness. Currently a placeholder — will be implemented in Phase 6.

## Planned Structure

```
tests/
├── test_products.py      # Product endpoint integration tests
├── test_orders.py        # Order endpoint integration tests
├── test_schemas.py       # Schema validation unit tests
└── conftest.py           # Shared fixtures (test DB, test client)
```

## How Testing Will Work

Tests will use FastAPI's `TestClient` to simulate HTTP requests without running the server:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products", json={
        "name": "Test Product",
        "description": "A product for testing",
        "category": "Testing",
        "price": 10.00,
        "stock_quantity": 5,
        "cost_price": 5.00
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"
```

> [!NOTE]
> Tests will use a separate temporary database to avoid corrupting development data.

## Real-World Analogy

Tests = **Quality inspection before shipping**. Before any code change goes live, the test suite runs to make sure nothing broke.

## 30-Second Revision

- `tests/` will contain pytest-based automated tests
- Uses FastAPI's `TestClient` for integration tests without a running server
- Separate test database to keep development data safe
- Coming in Phase 6 of the roadmap
