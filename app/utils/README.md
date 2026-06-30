# `app/utils/` — Shared Utilities & Helper Layer

> Reusable helper functions, validators, formatters, and logging routines that provide shared services across all layers of the application.

---

## 1. Files & Utilities

### `jwt.py`
Provides JWT token operations:
* Uses the `PyJWT` library to sign and decode stateless tokens.
* Maps `settings.secret_key` and `settings.algorithm` parameters dynamically.
* `create_jwt_token(data: dict) -> str`: Builds signed token strings with configured access token expiration claims (`exp`).
* `verify_jwt_token(token: str) -> dict | None`: Validates token signatures and returns decoded payload dictionaries, returning `None` if invalid.

### `logger.py`
Implements the centralized application logging context:
* Configures logging levels dynamically based on settings (`logging.DEBUG` vs `logging.INFO`).
* Stream formats log outputs: `[%(asctime)s] %(levelname)s in %(module)s: %(message)s`.
* Configures two distinct handlers:
  * Console handler streaming logs directly to `sys.stdout`.
  * File handler appending log lines to the persistent file [logs/app.log](file:///d:/ecommerce-api/logs/app.log).

### `response.py`
Provides a consistent response format for the client:
* `success_response(message: str, data: Any, status_code: int) -> JSONResponse`: Generates successful JSON responses with format `{"status": "success", "message": "...", "data": ...}`.
* `error_response(message: str, status_code: int, errors: Any) -> JSONResponse`: Generates error JSON responses with format `{"status": "fail", "message": "...", "errors": ...}`.

### `validators.py`
Implements sanitization rules for Pydantic schema validation:
* `strip_whitespace(v: str) -> str`: Trims leading and trailing spaces from strings.
* `lowercase_email(v: str) -> str`: Normalizes email addresses to lowercase.
* `prevent_empty(v: str) -> str`: Trims whitespace and throws `ValueError` if empty.
* `validate_password_strength(v: str) -> str`: Asserts password meets strength criteria (minimum 6 characters, at least 1 digit, and at least 1 letter).

---

## 2. When to Use Utils

Put a module in `utils/` when it represents a **cross-cutting service** that performs pure actions or formatting needed by multiple files. Keep helper functions pure (same inputs always produce the same outputs without mutating external state) to ensure they are easily testable.

---

## 3. 30-Second Revision

- **`utils/`** keeps code DRY by sharing helpers, validators, and logger templates.
- **`jwt.py`** uses PyJWT to sign and decode stateless tokens.
- **`logger.py`** pipes logs to the terminal and to `logs/app.log`.
- **`response.py`** formats unified success/fail JSON response envelopes.
- **`validators.py`** cleanses string inputs at the schema layer.
