# `app/middleware/` — Request Interception Layer

> Runs automatically on **every** request and response cycle. Used to intercept incoming requests, apply security policies, limit traffic, compress outputs, and record timing metrics.

---

## 1. Overview & Purpose

In professional web API engineering, **Middleware** handles cross-cutting concerns that apply globally across all endpoints.

Without middleware, if you wanted to measure request timing, limit requests, or log connections, you would need to duplicate that logic in every route handler. This violates the **DRY (Don't Repeat Yourself)** principle. 

### Core Responsibilities:
1. **Request Interception**: Inspects and records timestamps and IP metrics as soon as the HTTP request hits the server.
2. **Response Modification**: Modifies outgoing headers (e.g. injecting `X-Process-Time` or security headers) before yielding the bytes back to the client.
3. **Execution Safety**: Handles exceptions gracefully so that requests aren't left hanging in the event of crashes.
4. **Minimal Overhead**: Must execute extremely fast to prevent system-wide latency.

---

## 2. Request Timing Lifecycle

The request timing middleware intercepts the connection, measures execution duration, and attaches timing metadata to the response headers:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'nodeTextColor': '#1e293b', 'textColor': '#ffffff', 'titleColor': '#ffffff', 'edgeLabelBackground': '#1e293b', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#cbd5e1', 'actorBkg': '#f8fafc', 'actorBorder': '#cbd5e1', 'actorTextColor': '#1e293b', 'signalColor': '#4f46e5', 'signalTextColor': '#ffffff', 'labelColor': '#ffffff', 'loopTextColor': '#ffffff', 'noteBkgColor': '#fef08a', 'noteBorderColor': '#facc15', 'noteTextColor': '#713f12'}}}%%
sequenceDiagram
    autonumber
    actor Client
    participant Middleware as Request Timing Middleware
    participant App as Route / Controller

    Client->>Middleware: Incoming HTTP Request
    activate Middleware
    Note over Middleware: Record start_time (time.perf_counter())
    
    Middleware->>App: Forward Request via call_next()
    activate App
    App-->>Middleware: Yields HTTP Response
    deactivate App
    
    Note over Middleware: Record end_time & calculate process_time
    Note over Middleware: Add X-Process-Time response header
    Note over Middleware: Log execution stats to terminal and logs/app.log
    
    Middleware-->>Client: Return HTTP Response with timing header
    deactivate Middleware
```

---

## 3. Files & Implementations

### `timing.py`
Implements HTTP timing middleware:
* Measures processing time using a high-resolution clock (`time.perf_counter()`).
* Attaches the `X-Process-Time` response header.
* Logs the request method, path, and duration using the application `logger`.

### `security.py`
Implements secure HTTP response headers:
* Uses the `secure` package to inject default security headers (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`).
* Automatically bypasses documentation routes (`/docs`, `/redoc`, `/openapi.json`) to allow Swagger UI's external CDNs to render.

### `rate_limit.py`
Implements api traffic rate limiting:
* Uses `slowapi` to restrict requests mapped to client IP addresses (`100/15 minutes` by default).
* Registers the custom handler for `RateLimitExceeded` exceptions.

---

## 4. Key Design Patterns: ASGI & Middleware Call Stack

FastAPI middleware uses the **Chain of Responsibility** pattern. The middleware acts as a wrapper around the application.

1. **`call_next` Function**: The second parameter `call_next` is a callback function that represents the next middleware block or the target route handler. By invoking `await call_next(request)`, control is delegated down the stack.
2. **`time.perf_counter()` vs. `time.time()`**:
   * `time.time()` returns system epoch time (which can adjust or shift due to NTP synchronization).
   * `time.perf_counter()` returns a high-resolution monotonic clock specifically designed for measuring short durations, which is unaffected by system time adjustments.

---

## 5. Real-World Analogy

Think of middleware as the **Security Checkpoint Gate at a factory entrance**:
- Every delivery truck (request) passes through the gate on the way in.
- The guard records the license plate, stamps a timestamp on the manifest card (`start_time`), checks rate limits, and directs the truck to the loading bay (`call_next`).
- When the truck leaves the loading bay (response), the guard takes the manifest card, records the exit timestamp, calculates the total processing time, adds secure wrapper seals, and lets the truck leave.

---

## 6. Interview Questions & Tips

### 1. Why use middleware for request timing instead of putting timers inside every route?
Using middleware centralizes cross-cutting concerns. It ensures that timing, logging, CORS, or session validation are run automatically for **every request** without requiring developers to duplicate validation code in every route. This keeps route functions small, maintainable, and focused.

### 2. Can you access the request body (JSON payload) inside standard middleware?
Yes, but doing so consumes the request body stream. If you consume the stream without resetting it, the route handler downstream will find an empty body and fail with a `422 Unprocessable Entity` validation error. Reading request bodies in middleware should generally be avoided unless using specialized request-stream replacers.

### 3. What is the impact of slow middleware code?
Because middleware wraps every single API connection, any latency introduced inside middleware is multiplied across all endpoints. Middleware must be highly optimized, asynchronous, and non-blocking.

---

## 7. 30-Second Revision

- **Middleware** intercepts every request/response cycle globally.
- **`call_next`** yields control down the route execution stack.
- **`time.perf_counter()`** supplies monotonic high-resolution clock timing.
- **Security & Rate Limiting** are modularized and run in a decoupled fashion under `/app/middleware/`.
