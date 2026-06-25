# `app/controllers/` — Business Logic Layer

This folder contains the core decision-making code, database interactions, and business rules.

---

## 1. Purpose

> Why do we have a controllers folder?

In a clean architecture:
- **Isolate business logic**: Keep logic separated from HTTP/framework-specific routing code.
- **Enable reusability**: Multiple endpoints or CLI tasks can reuse the same controller functions.
- **Simplify unit testing**: You can test business operations directly by mocking database calls, without running the entire web server stack.

---

## 2. Responsibilities

### What belongs inside `controllers/`

- Reading and writing data to the database.
- Calculations (like summing order item costs).
- Domain rules (e.g., verifying if there is enough stock before completing an order).
- Constructing and returning schema responses.

### What does NOT belong inside `controllers/`

- Direct URL paths or decorators.
- Request headers, cookies, or HTTP parameters checks.

---

## 3. Files

### `product_controller.py`

- **Purpose**: Implements all actions related to product management.
- **Functions**:
  - `create_product(product: ProductCreate)`: Connects to the database, executes an `INSERT` statement, commits the transaction, and returns a `ProductResponse`.
  - `get_all_products()`: Retrieves all products, maps them to Pydantic responses, and closes the connection.
  - `get_product_by_id(product_id: int)`: Retrieves a single product by its ID, raises `ValueError` if not found, and closes the connection.
  - `delete_product(product_id: int)`: Deletes a product, verifies rowcount for existence check, and closes the connection.
- **When is it called**: Called by the `/products` route handler.
- **Who calls it**: `app/routes/products.py`.

### `order_controller.py`

- **Purpose**: Grouping business logic for order processing (like validating product stock and inserting entries).

---

## 4. Request Flow

The controller coordinates data exchange between routes and databases:

```
Client ──► Routes ──► app/controllers/  ◄── [Controller Layer]
                              │
                              ▼
                        database.py ──► SQLite DB
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

Controllers are where the real work gets done. If routes are the receptionists who verify forms, controllers are the managers who read the forms, check with the warehouse (database), perform calculations, update files, and write the final report.

---

## 6. Real-World Analogy

- **Controllers** = The manager/chef in a restaurant who actually cooks and manages ingredients.

---

## 7. Best Practices

### Do

- Close database resources correctly using context blocks or `finally` blocks.
- Perform internal state validation (e.g., check if a product exists before updating).

### Don't

- Import route objects or APIRouter into controllers.
- Access raw HTTP request objects unless absolutely necessary.

---

## 8. Interview Questions

1. **Why separate business logic from routes?**
   It allows you to test business logic independently of web framework details, reuse controllers, and maintain clean files.
2. **What is `cursor.lastrowid`?**
   It returns the row ID of the last row inserted into the database via SQLite, allowing you to return the created record ID instantly.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Direct SQLite SQL strings executed in controllers.

### Future Evolution
- **Phase 4**: Move SQL operations to a Repository layer. Controllers will interact only with Repositories instead of direct SQL.

---

## 10. Quick Revision

- `controllers/` houses all database operations and business logic.
- They are invoked by route files.
- They open and close database connections.
- They map database inputs into schema-friendly response outputs.
- Keeps routes clean and testable.
