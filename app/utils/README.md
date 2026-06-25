# `app/utils/` — Shared Helper Utilities

This folder holds helper functions, constants, and shared utilities used across different layers of the application.

---

## 1. Purpose

> Why do we have a utils folder?

To keep our codebase DRY (Don't Repeat Yourself):
- **Avoid code duplication**: Houses helper functions that don't belong to any specific controller or route.
- **Centralize constants**: Store configuration constants in one place rather than hardcoding strings.

---

## 2. Responsibilities

### What belongs inside `utils/`

- String formatter tools.
- Currency convertors.
- Shared domain constants (e.g. TAX_RATE, standard error messages).
- Timestamp formatting functions.

### What does NOT belong inside `utils/`

- Database connection configurations.
- Route controllers.

---

## 3. Files

### `constants.py`

- **Purpose**: Defines global fixed values (like tax rates, pagination limits, default page sizes) used throughout the system.
- **Who uses it**: Controllers, schemas, or routers needing static constants.

### `helpers.py`

- **Purpose**: Reusable logic utilities, such as price calculations or date formatting helper functions.

---

## 4. Request Flow

The utility layer does not occupy a single location in the request lifecycle; it is a shared utility layer imported across multiple components:

```
Routes ──────┐
             ├─► app/utils/ (constants, helpers)
Controllers ─┘
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

`utils` is your toolbox. If you have a small tool (like a calculator that formats prices or calculates tax rates) that is needed by both the cooks (controllers) and the front desk (routes), you store it in the utility toolbox so anyone can grab it whenever they need it.

---

## 6. Real-World Analogy

- **Utils** = The kitchen toolbox / shared tools.

---

## 7. Best Practices

### Do

- Keep helper functions simple and pure (no side effects).
- Document helpers with clear type hints.

### Don't

- Avoid importing routes or controllers inside `utils` to prevent circular dependencies.

---

## 8. Interview Questions

1. **What is a "pure function" and why are helpers often pure?**
   A function that always returns the same output for the same input and has no side effects. This makes it trivial to test and safe to reuse anywhere.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Empty modules ready for helpers.

---

## 10. Quick Revision

- `utils/` keeps code DRY by sharing helpers and constants.
- `constants.py` contains app-wide constants.
- `helpers.py` contains helper functions.
- Keep utilities pure, fast, and free of circular imports.
