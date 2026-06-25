# `app/utils/` — Shared Utilities

> Reusable helper functions and constants that don't belong to any specific controller or route.

## Files

### `constants.py`

App-wide fixed values like tax rates, pagination limits, and default page sizes. Currently a placeholder.

### `helpers.py`

Reusable logic utilities such as price calculations and date formatting. Currently a placeholder.

## When to Use Utils

Put something in `utils/` when it's needed by **multiple** controllers or routes and doesn't belong to any specific feature domain.

## Real-World Analogy

Utils = **The shared toolbox**. If both the electrician and the plumber need a wrench, it goes in the shared toolbox — not in either one's personal kit.

## Best Practices

**Do:** Keep helper functions pure (same input → same output, no side effects).

**Don't:** Import routes or controllers inside `utils/` — this causes circular imports.

## 30-Second Revision

- `utils/` keeps code DRY by sharing helpers and constants
- Helper functions should be pure and well-typed
- Never import routes or controllers from utils (circular dependency risk)
- Currently placeholder — will grow as the project evolves
