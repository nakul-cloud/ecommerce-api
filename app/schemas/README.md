# `app/schemas/` — Data Validation Layer

> Pydantic models that validate every request before your code runs and filter every response before it leaves the server.

## Why Schemas Matter

Without schemas, you'd write manual `if/else` checks for every field of every incoming request. Pydantic does this automatically — and generates Swagger documentation from the same definitions.

## Files

### `product_schema.py`

| Schema | Purpose | Key Fields |
|---|---|---|
| `ProductCreate` | Validates input for creating a product | `name` (3-100 chars), `price` (>0), `cost_price` (>0) |
| `ProductUpdate` | Validates partial updates (all fields optional) | Same fields as Create, but `Optional` |
| `ProductResponse` | Filters output — hides `cost_price` | `id`, `name`, `description`, `category`, `price`, `stock_quantity` |

### `order_schema.py`

| Schema | Purpose | Key Fields |
|---|---|---|
| `OrderItem` | Represents one product in an order | `product_id` (>0), `quantity` (>0) |
| `OrderCreate` | Validates a new order with multiple items | `items` (List[OrderItem], min 1 item) |
| `OrderResponse` | Returns order details to the client | `id`, `total_amount`, `items` |

### `internal_schemas.py`

Contains internal Pydantic models used inside controllers and services to pass structured data between application layers without exposing them to public API clients.

| Schema | Purpose | Key Fields |
|---|---|---|
| `ValidatedOrderItem` | Stores resolved product details (including unit price) after database validation in `create_order` | `product_id`, `quantity`, `unit_price` |

> [!NOTE]
> **Internal vs. Public Schemas**:
> Public API models (like `OrderItem`) only contain inputs provided by clients (e.g. they don't supply prices to prevent price manipulation). `ValidatedOrderItem` is constructed internally by the controller after fetching prices from the database, allowing us to maintain strict type safety when passing validated item lists around.

## The Input ≠ Output Pattern

This is a critical security pattern:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#e2e8f0', 'titleColor': '#1e293b', 'edgeLabelBackground': '#ffffff', 'textColor': '#334155'}}}%%
flowchart TD
    subgraph ClientRequest [Client Request JSON]
        R1[name]
        R2[description]
        R3[category]
        R4[price]
        R5[stock_quantity]
        R6[cost_price]
    end

    subgraph Validation [ProductCreate Schema]
        direction TB
        V1[Validates Types & Lengths]
    end

    subgraph Database [SQLite DB]
        D1[(Database Record)]
        D2[id]
        D3[name]
        D4[description]
        D5[category]
        D6[price]
        D7[stock_quantity]
        D8[cost_price]
    end

    subgraph Response [ProductResponse Schema]
        direction TB
        Out1[id]
        Out2[name]
        Out3[description]
        Out4[category]
        Out5[price]
        Out6[stock_quantity]
        Note1[cost_price is REMOVED]
    end

    ClientRequest -->|Pydantic parses| Validation
    Validation -->|Inserts data| Database
    Database -->|Selects data| Response
    D8 -.->|Excluded| Note1
```

> [!IMPORTANT]
> The response schema acts as a security filter. `cost_price` is stored in the database but never exposed to API consumers. This is how real companies protect internal pricing data.

## Request Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8', 'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b', 'background': '#ffffff', 'mainBkg': '#f8fafc', 'nodeBorder': '#cbd5e1', 'clusterBkg': '#f1f5f9', 'clusterBorder': '#e2e8f0', 'titleColor': '#1e293b', 'edgeLabelBackground': '#ffffff', 'textColor': '#334155'}}}%%
flowchart LR
    Client([Client]) -->|Request Data| InSchema[Pydantic Input Schema]
    InSchema -->|Validate & Parse| Controller[Controller Layer]
    Controller -->|Query / Insert| DB[(SQLite DB)]
    DB -->|Raw Data| Controller
    Controller -->|Data Object| OutSchema[Pydantic Output Schema]
    OutSchema -->|Filter & Serialize| Client
    
    style InSchema fill:#4f46e5,stroke:#3730a3,color:#ffffff
    style OutSchema fill:#4f46e5,stroke:#3730a3,color:#ffffff
```

## Real-World Analogy

Schemas = **Application forms**. They specify required fields, data types, and rules. If the form is filled incorrectly, the receptionist rejects it immediately. The manager (controller) never sees invalid data.

## Best Practices

**Do:** Use `Field(gt=0)` constraints. Document fields with `description=`. Keep input and output schemas separate.

**Don't:** Include sensitive fields in Response schemas. Don't put business logic in validators.

## 30-Second Revision

- Schemas validate requests (input) and filter responses (output)
- Internal schemas (in `internal_schemas.py`) handle structured data validation between internal components/controllers without being exposed to clients
- Pydantic auto-returns `422 Unprocessable Entity` for validation failures
- Response schemas hide internal fields like `cost_price` from API consumers
- `Field(...)` means required, `Field(None)` means optional
- `gt=0` means greater than zero, `min_length=3` means at least 3 characters
