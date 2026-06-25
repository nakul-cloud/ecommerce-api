# `app/` — Application Package

> The entire API lives here. Every subfolder has exactly one responsibility.

## Overview

In professional backend engineering, you never put everything in one file. The `app/` package organizes code by responsibility so that adding a new feature means adding files to the right folders — not scrolling through a 2000-line `main.py`.

## How It Works

```
app/
├── main.py              Entry point — creates the app, wires routers, registers handlers
├── config/              Settings and database connection
├── routes/              HTTP endpoint definitions (URL → handler mapping)
├── controllers/         Business logic and database operations
├── schemas/             Pydantic models for request/response validation
├── exceptions/          Custom exceptions and global error handlers
├── middleware/           Request/response interceptors (timing, CORS)
└── utils/               Shared helper functions and constants
```

## Request Flow

When a request hits the API, it flows through these layers:

```
Client ──► Middleware ──► Route ──► Schema (validate) ──► Controller ──► Database
                                                                           │
Client ◄── Middleware ◄── Route ◄── Schema (filter) ◄── Controller ◄───────┘
```

If a business error occurs (e.g. product not found), the controller raises a custom exception. The global exception handler intercepts it and returns a clean JSON error response.

## Files

### `__init__.py`

Makes `app/` a Python package. Without this file, `from app.config.settings import APP_NAME` would fail with `ModuleNotFoundError`. It's empty, but essential.

### `main.py`

The wiring diagram of the entire application. It does four things:

1. Creates the FastAPI instance with settings from `.env`
2. Registers global exception handlers
3. Creates database tables on startup
4. Connects route modules to the app

> [!TIP]
> `main.py` should stay short. If it's longer than 50 lines, logic that belongs in a controller or middleware has leaked in.

## Real-World Analogy

Think of `app/` as a **hospital**:

| Folder | Hospital Equivalent |
|---|---|
| `main.py` | The building itself |
| `config/` | Power supply and medical records system |
| `routes/` | Reception desk — directs patients |
| `controllers/` | Doctors — diagnose and treat |
| `schemas/` | Intake forms — verify patient information |
| `exceptions/` | Emergency protocols — handle when things go wrong |
| `middleware/` | Security checkpoint at the entrance |
| `utils/` | Shared medical instruments |

## Best Practices

**Do:**
- Keep `main.py` minimal — wiring only
- Import with full paths: `from app.config.settings import APP_NAME`
- Create `__init__.py` in every sub-package

**Don't:**
- Put database queries in `main.py`
- Put route decorators in controllers
- Put business logic in schemas

## 30-Second Revision

- `app/` is the main Python package — all application code lives here
- `main.py` creates the FastAPI app, registers handlers, connects routers
- Each sub-package has one responsibility (Single Responsibility Principle)
- `__init__.py` is empty but must exist for Python imports to work
- Request flows: Client → Middleware → Route → Schema → Controller → Database → Response
