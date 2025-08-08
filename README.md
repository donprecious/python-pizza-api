# Usersnack Backend (FastAPI) — Implementation Plan

This document outlines the implementation plan, architecture, and technical decisions for the Usersnack backend API.

## 0) TL;DR (Scope & Non-Goals)

Build a clean, scalable API to: browse catalog (pizzas, extras), manage carts (email or cart_token), compute quotes, and create orders.

**Not in MVP:** auth, payments, inventory, tax/fees, delivery estimates.

**Two pragmatic extras:**
- API versioning: `/api/v1`
- Idempotency for key POSTs via `Idempotency-Key`

## 1) Architecture & Tech

### 1.1 Style
- Clean/Hexagonal Architecture
- HTTP (routers) → Services (use-cases) → Repositories (DB) → PostgreSQL
- Domain logic isolated from frameworks. DTOs separate from ORM models.

### 1.2 Stack
- Python 3.12, FastAPI (ASGI)
- Pydantic v2 (schemas & validation)
- SQLAlchemy 2.x (async) + PostgreSQL
- Alembic (migrations)
- `structlog` (JSON logging)
- `slowapi` (rate limits) [or plug-compatible]
- `pytest`, `pytest-asyncio`, `httpx` (tests), `testcontainers-postgres`
- `ruff` (lint/format), `mypy` (types)
- Docker (multi-stage), docker compose
- `pydantic-settings` (.env, 12-factor)

## 2) Requirements & Decisions

- **Cart identity:** exactly one of `X-Cart-Email: <email>` or `X-Cart-Token: <uuid>`
- **Optional helper:** `POST /carts/init` → returns `cart_token`.
- **Pricing policy:** always re-price from current catalog for cart reads, quotes, and checkout.
- **Taxes/fees:** none (totals == subtotal).
- **Currency:** default USD (configurable).
- **Extras:** all extras valid for all pizzas (MVP).
- **Pizza prices:** single base price per pizza (no sizes) in MVP.

## 3) Project Structure

```
usersnack/
  app/
    api/
      v1/
        pizzas.py         # GET /pizzas, /pizzas/{id}
        extras.py         # GET /extras
        carts.py          # POST/GET/PATCH/DELETE carts, checkout
        orders.py         # POST /orders, POST /orders:quote, GET /orders/{id}
        health.py         # GET /health
    core/
      config.py           # pydantic-settings
      logging.py          # structlog init
      middleware.py       # request_id, timing
      security.py         # CORS, headers
      response.py         # ok(), paginated(), error()
      errors.py           # AppError hierarchy
      exception_handler.py# global exception mapping -> envelope
      idempotency.py      # helpers + policy
      pagination.py
      validation.py       # shared validators (email/token XOR, etc.)
    domain/
      models.py           # domain types (dataclasses/typing)
      price_rules.py      # PriceCalculator (Decimal, rounding)
    schemas/
      common.py
      catalog.py          # PizzaOut, ExtraOut
      cart.py             # CartItemIn, CartOut, etc.
      order.py            # OrderIn, OrderOut, QuoteOut
    services/
      catalog_service.py  # read-only
      cart_service.py     # add/get/update/remove/clear/checkout
      order_service.py    # direct order, quote, get
    repos/
      base.py             # session helpers
      pizza_repo.py
      extra_repo.py
      cart_repo.py
      order_repo.py
      idempotency_repo.py
    events/
      bus.py              # in-process event bus
      handlers.py         # stub subscribers
      models.py           # CartUpdated, OrderCreated...
    db/
      models.py           # SQLAlchemy ORM
      session.py          # async engine/session factory
      seed.py             # seeding utilities
    main.py               # app factory (create_app)
  scripts/
    seed_from_data.py     # load pizzas/extras from dataset
  migrations/             # Alembic
  tests/
    unit/                 # domain & services
    api/                  # httpx AsyncClient
    repos/                # with Testcontainers Postgres
    e2e/                  # compose-up smoke tests
  docker/
    Dockerfile
    docker-compose.yml
  .env.example
  Makefile
  README.md
```

## 4) Data Model (DB/ERD)

- **Pizza**: `id` UUID PK | `name` text | `base_price` numeric(12,2) | `image_url` text | `is_active` bool default true | `created_at` timestamptz
- **Extra**: `id` UUID PK | `name` text unique | `price` numeric(12,2) | `is_active` bool | `created_at` timestamptz
- **Cart**: `id` UUID PK | `email` text NULL unique | `cart_token` uuid NULL unique | `created_at` | `updated_at`. CHECK (exactly one of email/cart_token is not null).
- **CartItem**: `id` UUID PK | `cart_id` FK | `pizza_id` FK | `quantity` int | `selected_extras` jsonb. (We don’t store prices in cart—always re-price on read.)
- **Order**: `id` UUID PK | `email` text | `status` text | `subtotal` numeric | `extras_total` numeric | `grand_total` numeric | `customer_info` jsonb | `created_at`
- **OrderItem**: `id` UUID PK | `order_id` FK | `pizza_id` FK | `quantity` int | `selected_extras` jsonb | `unit_base_price` numeric | `unit_extras_total` numeric | `line_total` numeric. (Orders do store prices for audit/history.)
- **Idempotency**: `key` text PK | `request_hash` text | `response_body` jsonb | `status_code` int | `created_at` timestamptz

**Indexes:**
- `Pizza(is_active)`, `Extra(is_active)`
- `Cart(email)` unique, `Cart(cart_token)` unique
- `CartItem(cart_id)`, `Order(created_at)`, `Order(email)`

## 5) API Design

### 5.1 Conventions
- **Base path:** `/api/v1`
- **Media type:** JSON (UTF-8)
- **Response envelope:** (see §6)
- **Idempotency:** `Idempotency-Key` on `POST /carts/items`, `POST /orders`, `POST /carts/checkout`
- **Cart identity:** exactly one of `X-Cart-Email: <email>` OR `X-Cart-Token: <uuid>`

### 5.2 Endpoints
- **Health:** `GET /health`
- **Catalog:** `GET /pizzas`, `GET /pizzas/{pizza_id}`, `GET /extras`
- **Cart:** `POST /carts/init`, `POST /carts/items`, `GET /carts`, `PATCH /carts/items/{item_id}`, `DELETE /carts/items/{item_id}`, `DELETE /carts`, `POST /carts/checkout`
- **Orders:** `POST /orders`, `POST /orders:quote`, `GET /orders/{order_id}`

### 5.3 Pagination
- **Query:** `?page=1&size=20` (max size 100)
- **Envelope:** includes `meta.page`, `meta.size`, `meta.total`.

## 6) Response Envelope & Error Model

### 6.1 Success
```json
{
  "success": true,
  "data": { /* endpoint payload */ },
  "meta": {
    "request_id": "9b0c…",
    "timestamp": "2025-08-07T21:00:00Z",
    "page": 1,
    "size": 20,
    "total": 57
  }
}
```

### 6.2 Error
```json
{
  "success": false,
  "error": {
    "code": "validation_error",
    "title": "Validation failed",
    "detail": "One or more fields are invalid.",
    "field_errors": { "quantity": ["Must be >= 1"] }
  },
  "meta": { "request_id": "9b0c…", "timestamp": "…" }
}
```
- Helpers in `app/core/response.py`: `ok()`, `paginated()`, `error()`.

## 7) Validation (API + Business)
- Pydantic v2 for types, list uniqueness, cross-field checks.
- Service-level checks for existence, activity, quantity bounds, etc.
- Invalid input → `ValidationAppError` (422) or `InvalidIdentityAppError` (400).

## 8) Pricing Rules (`domain/price_rules.py`)
- No tax/fees.
- Money uses `Decimal` with `ROUND_HALF_EVEN` to 2 dp.
- Re-priced for `GET /carts`, `POST /orders`, `POST /orders:quote`, and `POST /carts/checkout`.

## 9) Domain Events
- **Events:** `CartUpdated`, `OrderCreated`, `QuoteRequested`
- **Bus & Handlers:** In-process async `EventBus`. Handlers for logging/stubs.

## 10) Exceptions & Global Handler
- **Hierarchy:** `AppError` base class with specific sub-classes (`ValidationAppError`, `NotFoundAppError`, etc.)
- **Handler:** Maps `AppError` to the error envelope, handles Pydantic errors, and has a catch-all for 500s.

## 11) Logging & Observability
- `structlog` for JSON logs with `request_id`, timing, etc.
- Middleware for `request_id` and timing.

## 12) Security & Hardening
- CORS restricted to configured origins.
- Standard security headers.
- Rate limiting on key POST endpoints.
- Idempotency key handling.

## 13) DevEx & Config
- `Makefile` for common tasks (`dev`, `lint`, `test`, etc.).
- `.env.example` for configuration.
- Multi-stage Dockerfile and `docker-compose.yml`.

## 14) Testing Strategy
- **Unit:** `price_rules`, `cart_service`, `order_service`.
- **API:** `httpx` against app factory for happy/error paths.
- **Integration:** `Testcontainers` for Postgres-dependent repos.
- **Coverage:** 80%+ overall; 95%+ on services & pricing.

## 15) CI/CD
- **CI (GitHub Actions):** Lint, format, type check, test, build Docker image.
- **CD:** Deploy to a target like Azure/Render/Fly/AWS, run migrations.

## 16) Acceptance Criteria (Key)
- All responses use the standard envelope.
- Cart identity XOR is enforced.
- Re-pricing logic is correct and consistently applied.
- Idempotency works as expected.
- Delete operations are functional.
- Tests pass and meet coverage targets.
- Logs are structured and contain no PII.

## 17) OpenAPI Sketch (excerpt)
- Full spec will be generated from code and available at `/docs`.

## 18) Milestones & Backlog
- **M0 – Scaffold:** App factory, config, logging, DB session, CI, Docker.
- **M1 – Catalog:** Repos, services, routers for pizzas and extras.
- **M2 – Cart:** Full cart lifecycle implementation.
- **M3 – Orders & Quote:** Direct order, quote, and retrieval.
- **M4 – Hardening:** Rate limits, E2E tests, docs polish.

## 19) Example Flows
- **Anonymous cart:** `init` → `add items` → `get cart` → `checkout`.
- **Direct order:** `quote` (optional) → `create order` → `get order`.