# `tests/` — Automated Testing Suite

This folder holds unit and integration tests to verify application correctness automatically.

---

## 1. Purpose

> Why do we have a tests folder?

To guarantee code quality and stability:
- **Prevent regressions**: Ensure that new features or refactors don't break existing functionality.
- **Support automatic testing**: Enable running test runners like `pytest` to validate routes, schemas, and controllers before deployment.

---

## 2. Responsibilities

### What belongs inside `tests/`

- Unit tests targeting schemas and helper functions.
- Integration tests targeting FastAPI routes and controller behaviors.
- Test configurations (`conftest.py`) and mock database fixtures.

### What does NOT belong inside `tests/`

- Actual application production code or routes.

---

## 3. Request Flow

Tests bypass the live client route, simulating API requests locally:

```
[Pytest Runner] ──► Test Client ──► Routes ──► Controllers ──► Test DB
```

---

## 4. Beginner Explanation

"If I forget this after six months..."

This is the quality control inspection room. Before shipping code changes to real customers, we run test scripts in this folder to make sure products can still be created, orders can be made, and constraints aren't broken.

---

## 5. Real-World Analogy

- **Tests** = The safety inspector testing products before they leave the factory.

---

## 6. Best Practices

### Do

- Use a separate temporary database for tests so you don't overwrite your dev data.
- Run tests regularly before committing new features.
- Keep tests isolated so they don't depend on each other.

### Don't

- Never run tests directly against your production or development database file.

---

## 7. Interview Questions

1. **Why use a separate database for testing?**
   To avoid corrupting or wiping out development or production records, and to ensure each test starts with a clean database state.
2. **What is Pytest?**
   A popular Python testing framework that makes it easy to write simple, readable, and scalable unit and integration tests.

---

## 8. Learning Notes

### Current Phase (Phase 1)
- Empty folder ready for test cases.

### Future Evolution
- **Phase 6**: Write integration tests using FastAPI's `TestClient` and mock database fixtures.

---

## 9. Quick Revision

- `tests/` contains validation scripts.
- Pytest is the main test runner.
- Verifies endpoints and business logic without manual testing.
- Uses independent test database connections.
