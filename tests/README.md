# `tests/` — Automated Test Suite & Quality Assurance

> The test layer containing test fixtures, automated unit tests, and HTTP integration suites to guarantee API contract compliance and regression safety.

---

## 1. Purpose

Reliable systems require automated validation. The `tests/` directory is designed to house our test suites powered by **pytest** and FastAPI's built-in **TestClient**. 

Automated testing ensures:
- **Contract Enforcement**: Changing controller logic won't accidentally alter API response schemas and break frontend consumers.
- **Regression Prevention**: Code changes, package updates, or refactorings can be validated instantly.
- **Auth Guard Verification**: Ensuring restricted roles (e.g. admin-only endpoints) reject unauthorized or invalid tokens.
- **Mock Safety**: Validating business logic behavior under simulated network or resource exceptions.

---

## 2. Test Architecture & Dependency Injection

FastAPI's architecture shines in test environments because of its native **Dependency Injection** system. We can override active dependencies (like database connections or authentication checkers) dynamically during a test run without modifying the source code.

```
                    ┌────────────────────────────┐
                    │      Pytest Runner         │
                    └────────────────────────────┘
                                   │
                                   ▼
                   ┌──────────────────────────────┐
                   │    conftest.py (Fixtures)    │
                   └──────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌──────────────────┐                                ┌──────────────────┐
│   Test Database  │                                │  API Test Client │
│ (Temporary File) │                                │  (TestClient)    │
└──────────────────┘                                └──────────────────┘
         │                                                   │
         │ (Override database connection)                     │ (Simulate HTTP requests)
         ▼                                                   ▼
┌──────────────────┐                                ┌──────────────────┐
│ app.dependency_   │                                │  app.main (APP)  │
│    overrides     │                                │                  │
└──────────────────┘                                └──────────────────┘
```

### Key Setup Patterns (Phase 6 implementation plan)

1. **`conftest.py`**: A special pytest file that shares fixtures across all test files. This file will host the setup and teardown logic for the temporary SQLite database and the FastAPI test client.
2. **Dependency Overrides**: In our tests, we will override the database connection function:
   ```python
   from app.main import app
   from app.config.database import get_db
   
   # Overriding the database dependency to use a clean test database
   app.dependency_overrides[get_db] = get_test_db
   ```
3. **Mocking JWT Auth**: Rather than logging in and fetching tokens via HTTP before every test, we can override the authentication dependency `get_current_user` to yield a mock user with specific roles directly.

---

## 3. Planned Structure & File Directory

When implemented in Phase 6, the test suite will follow this structure:

```
tests/
├── conftest.py               # Shared test fixtures (test client, test database setup/teardown)
├── test_products.py          # Integration tests for /products CRUD endpoints (Admin vs Customer roles)
├── test_orders.py            # Integration tests for /orders: stock checks, total calculations, transaction safety
├── test_auth.py              # Unit & integration tests for password hashing, login, and JWT verification
└── test_schemas.py           # Unit tests validating Pydantic constraints (e.g., negative prices, email format)
```

---

## 4. Test Example (How Testing Works)

An integration test simulates actual HTTP requests hitting the router, running through the validation, exception, and controller layers:

```python
import pytest
from fastapi.testclient import TestClient

def test_create_product_as_admin(client: TestClient, admin_token_headers: dict):
    # GIVEN: A payload containing a new product
    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "category": "Electronics",
        "price": 89.99,
        "stock_quantity": 40,
        "cost_price": 45.00
    }
    
    # WHEN: An admin posts to the product creation endpoint
    response = client.post("/products", json=payload, headers=admin_token_headers)
    
    # THEN: The response should be 201 Created and return the filtered response schema
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mechanical Keyboard"
    assert "cost_price" not in data  # Verifying that internal data is filtered out
```

---

## 5. Interview Questions & Tips

### 1. What is the difference between Unit Tests, Integration Tests, and E2E Tests?
* **Unit Tests**: Test a single isolated function or class (e.g., testing that `verify_password` returns false for incorrect credentials). They do not hit databases or network sockets.
* **Integration Tests**: Verify that multiple layers (routing, validation schemas, controllers, and database queries) interact correctly together.
* **End-to-End (E2E) Tests**: Test the entire application flow from the user interface down to external services, simulating complete user behaviors.

### 2. Why shouldn't tests write to the development SQLite database?
Running tests against the live development database risks:
- **Data Pollution**: Leaving behind test records (e.g. "Test Product") which mess up manual testing and UI views.
- **Flaky Tests**: Run order dependencies. If one test deletes database rows, another test might fail unexpectedly because it relied on that data.
- **Race Conditions**: If development and testing run concurrently, writes from one process will lock the database file and cause the other process to fail.

### 3. How do you mock external API calls or databases in Python tests?
We use `unittest.mock` (with `Mock` or `MagicMock`) or pytest-mock (`mocker` fixture) to patch third-party service calls. Mocking allows us to replace slow, volatile network requests (like an external payment gateway) with a dummy object that returns a predictable response, ensuring tests run fast, offline, and reliably.

---

## 6. 30-Second Revision

- **`tests/`** contains pytest files checking code correctness and api responses.
- **`conftest.py`** configures shared environments (e.g., clean temporary test databases).
- **FastAPI `dependency_overrides`** make it trivial to swap out production dependencies for mocked versions during testing.
- **Test Isolation**: Every test run should start with a clean database state and run independently of other tests.
- **Implementation**: Scheduled for **Phase 6** of the project roadmap.
