# `app/middleware/` — Request Interception Layer

> Runs on **every** request. Used for timing, logging, authentication, and CORS — things that apply globally.

## Why Middleware?

Without middleware, you'd add timing/logging/auth code to every single route handler. Middleware centralizes cross-cutting concerns so they run automatically on all requests.

## Files

### `timing.py`

Measures and logs execution duration of every API request, and adds the duration to response headers.

**How it works:**

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'nodeTextColor': '#1e293b', 'textColor': '#ffffff', 'titleColor': '#ffffff', 'edgeLabelBackground': '#1e293b', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#e2e8f0', 'actorBkg': '#f8fafc', 'actorBorder': '#cbd5e1', 'actorTextColor': '#1e293b', 'signalColor': '#4f46e5', 'signalTextColor': '#ffffff', 'noteBkgColor': '#fef08a', 'noteBorderColor': '#facc15', 'noteTextColor': '#713f12'}}}%%
sequenceDiagram
    autonumber
    actor Client
    participant Middleware as Request Timing Middleware
    participant App as Route / Controller

    Client->>Middleware: Incoming HTTP Request
    activate Middleware
    Note over Middleware: Record start_time (time.perf_counter())
    
    Middleware->>App: Forward Request
    activate App
    App-->>Middleware: Return HTTP Response
    deactivate App
    
    Note over Middleware: Record end_time & calculate process_time
    Note over Middleware: Add X-Process-Time response header
    Note over Middleware: Log method, path, and duration to terminal
    
    Middleware-->>Client: Return HTTP Response with timing header
    deactivate Middleware
```

## Real-World Analogy

Middleware = **Security gate at a building entrance**. Every visitor passes through on the way in (request) and on the way out (response). The guard logs entry time, checks credentials, and records exit time.

## Best Practices

**Do:** Keep middleware execution extremely fast — slow middleware slows every request.

**Don't:** Put database queries in middleware. Don't read the request body unless necessary.

## 30-Second Revision

- Middleware runs on every request/response cycle
- Used for timing, logging, CORS, rate limiting, authentication
- Must be fast — adds latency to every single endpoint
- Implemented to add custom `X-Process-Time` response header and terminal logging

## Interview Tip

> [!TIP]
> **Why do we use middleware for request timing instead of putting timers inside every route?**
>
> "Middleware runs for every request automatically. By measuring time in one place, I avoid duplicating timing logic across every route, making the code cleaner, easier to maintain, and ensuring consistent performance monitoring throughout the application."
