# `app/middleware/` — Request Interception Layer

This folder houses middleware classes that process requests and responses globally.

---

## 1. Purpose

> Why do we have a middleware folder?

Middleware handles cross-cutting concerns that apply globally to all endpoints:
- **Global interception**: Inspect, block, or modify requests before they reach routes.
- **Global processing**: Inject headers, run timings, or log status codes after responses are generated.

Without middleware, you would have to manually add log statements, authentication checks, or timing logic to every routing endpoint.

---

## 2. Responsibilities

### What belongs inside `middleware/`

- CORS (Cross-Origin Resource Sharing) middleware configurations.
- Execution metrics tracking (e.g. logging execution duration).
- Global request loggers.

### What does NOT belong inside `middleware/`

- Core business logic.
- Route-specific parameters validations.

---

## 3. Files

### `timing.py`

- **Purpose**: Measures and logs the execution duration of every API request.
- **When is it called**: Runs immediately when a request enters the application, and resumes once the route finishes execution to calculate runtime.
- **Who calls it**: FastAPI's internal middleware execution chain.

---

## 4. Request Flow

Middleware forms a protective wrap around the routing endpoints:

```
Client (Request) ──► [Middleware (Start timer)] ──► Routes ──► Controllers
                                                                  │
                                                                  ▼
Client (Response) ◄── [Middleware (Log time + header)] ◄──────────┘
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

Middleware is like the security gate at the front of a corporate office. Every visitor (request) must pass through it on the way in, where security logs their entry time. When the visitor leaves (response), they pass the same gate, where security logs their exit time and calculates how long they spent inside.

---

## 6. Real-World Analogy

- **Middleware** = Security guard at the building entrance.

---

## 7. Best Practices

### Do

- Keep middleware execution extremely fast — slow middleware slows down every single API request.
- Handle exceptions inside middleware so the response cycle finishes cleanly.

### Don't

- Avoid reading or modifying the request body inside middleware unless necessary, as it can exhaust request streams.

---

## 8. Interview Questions

1. **What is middleware?**
   A function or class that runs before every request is processed, and after every response is generated.
2. **What is a risk of putting database queries in middleware?**
   It runs on every request. If not designed carefully, it can exhaust database connections or severely slow down the API.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Initial placeholders.

### Future Evolution
- **Phase 3**: Request timing logger.
- **Phase 5**: Rate limiting middleware implementation.

---

## 10. Quick Revision

- `middleware/` executes operations globally on all HTTP requests.
- `timing.py` captures request/response execution duration.
- Good for logging, authentication headers, CORS, and rate limiting.
- Must execute fast to avoid adding latency to endpoints.
