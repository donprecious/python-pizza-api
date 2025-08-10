# Pizza Ordering API

A comprehensive FastAPI-based backend service for a pizza ordering system, implementing Clean Architecture principles with modern Python technologies.

## Table of Contents

- [Architecture & Design](#architecture--design)
- [Technologies & Tools](#technologies--tools)
- [API Features](#api-features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Testing Documentation](#testing-documentation)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Configuration](#configuration)

## Architecture & Design

### Clean Architecture Implementation

This project follows Clean Architecture principles with clear separation of concerns:

- **API Layer** ([`app/api/routers/`](app/api/routers/)): FastAPI routers handling HTTP requests and responses
- **Service Layer** ([`app/services/`](app/services/)): Business logic and use cases
- **Repository Layer** ([`app/db/repositories/`](app/db/repositories/)): Data access abstraction
- **Database Layer** ([`app/db/models.py`](app/db/models.py)): SQLAlchemy ORM models

### Repository Pattern with Unit of Work

The application implements the Repository pattern with Unit of Work for data access:

- **Unit of Work** ([`app/db/uow.py`](app/db/uow.py)): Manages database transactions and coordinates repositories
- **Repositories**: Abstract data access for each entity (Pizza, Extra, Cart, Order, Customer)
- **Transaction Management**: Automatic commit/rollback with async context managers

### Service Layer Architecture

Business logic is encapsulated in service classes:

- [`CartService`](app/services/cart_service.py): Cart management and checkout operations
- [`CatalogService`](app/services/catalog_service.py): Pizza and extras catalog operations
- [`OrderService`](app/services/order_service.py): Order creation and management

### Database Design with SQLAlchemy

- **Async SQLAlchemy 2.x**: Modern async ORM with type hints
- **UUID Primary Keys**: All entities use UUID for better scalability
- **Relationship Mapping**: Proper foreign key relationships between entities
- **Base Model**: Common fields (id, created_at, updated_at) in [`BaseModel`](app/db/base.py)

## Technologies & Tools

### Core Framework
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Python 3.12+**: Latest Python features and performance improvements
- **Uvicorn**: ASGI server for production deployment

### Database & ORM
- **PostgreSQL**: Robust relational database
- **SQLAlchemy 2.x**: Async ORM with type hints
- **Alembic**: Database migration management
- **Psycopg**: PostgreSQL adapter for Python

### Data Validation & Serialization
- **Pydantic v2**: Data validation and serialization with type hints
- **Pydantic Settings**: Environment-based configuration management

### Development & Quality
- **Poetry**: Dependency management and packaging
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Structlog**: Structured logging with JSON output

### Testing
- **Pytest**: Testing framework with async support
- **Pytest-asyncio**: Async test support
- **HTTPX**: Async HTTP client for API testing
- **Testcontainers**: Integration testing with real PostgreSQL
- **Pytest-mock**: Mocking utilities for unit tests

### Infrastructure
- **Docker**: Containerization with multi-stage builds
- **Docker Compose**: Local development environment
- **Slowapi**: Rate limiting middleware

## API Features

### Pizza Catalog Management
- Browse available pizzas with filtering capabilities
- View detailed pizza information including ingredients and pricing
- Manage pizza extras and add-ons
- Support for active/inactive status

### Shopping Cart Operations
- Create and manage shopping carts with unique identifiers
- Add pizzas with customizable extras to cart
- Real-time price calculation based on current catalog prices
- Cart persistence across sessions

### Order Processing
- Convert carts to orders with customer information
- Order status tracking and management
- Detailed order history with line items
- Price snapshot preservation for audit trails

### Customer Management
- Customer information storage and retrieval
- Order history tracking per customer
- Flexible customer identification system

### Advanced Features
- **Pagination**: Configurable pagination for list endpoints
- **Rate Limiting**: Protection against API abuse
- **Structured Logging**: JSON-formatted logs with request tracking
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Data Seeding**: Automatic database seeding with sample data

## Project Structure

```
usersnack/
├── app/                          # Main application package
│   ├── api/                      # API layer
│   │   ├── deps.py              # Dependency injection
│   │   └── routers/             # FastAPI routers
│   │       ├── carts.py         # Cart management endpoints
│   │       ├── extras.py        # Extras catalog endpoints
│   │       ├── health.py        # Health check endpoint
│   │       ├── orders.py        # Order management endpoints
│   │       └── pizzas.py        # Pizza catalog endpoints
│   ├── core/                     # Core utilities and configuration
│   │   ├── config.py            # Application configuration
│   │   ├── exception_handler.py # Global exception handling
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── limiter.py           # Rate limiting configuration
│   │   ├── logging.py           # Structured logging setup
│   │   ├── price_rules.py       # Pricing calculation logic
│   │   └── response.py          # Response formatting utilities
│   ├── db/                       # Database layer
│   │   ├── base.py              # Base model with common fields
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── session.py           # Database session management
│   │   ├── uow.py               # Unit of Work implementation
│   │   └── repositories/        # Repository pattern implementation
│   │       ├── cart_repo.py     # Cart data access
│   │       ├── customer_repo.py # Customer data access
│   │       ├── extra_repo.py    # Extra data access
│   │       ├── order_repo.py    # Order data access
│   │       └── pizza_repo.py    # Pizza data access
│   ├── schemas/                  # Pydantic schemas for validation
│   │   ├── cart.py              # Cart-related schemas
│   │   ├── catalog.py           # Catalog schemas
│   │   ├── customer.py          # Customer schemas
│   │   ├── order.py             # Order schemas
│   │   └── pagination.py        # Pagination schemas
│   └── services/                 # Business logic layer
│       ├── cart_service.py      # Cart business logic
│       ├── catalog_service.py   # Catalog business logic
│       └── order_service.py     # Order business logic
├── docker/                       # Docker configuration
│   ├── Dockerfile               # Multi-stage Docker build
│   └── docker-compose.yml       # Local development setup
├── migrations/                   # Alembic database migrations
│   ├── env.py                   # Alembic environment configuration
│   └── versions/                # Migration files
├── scripts/                      # Utility scripts
│   └── seed.py                  # Database seeding utilities
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── e2e/                     # End-to-end tests
│   │   ├── conftest.py          # E2E test configuration
│   │   └── test_api.py          # API integration tests
│   └── unit/                    # Unit tests
│       ├── test_cart_service.py # Cart service unit tests
│       ├── test_catalog_service.py # Catalog service unit tests
│       └── test_order_service.py # Order service unit tests
├── .env.example                  # Environment variables template
├── alembic.ini                   # Alembic configuration
├── main.py                       # Application entry point
├── Makefile                      # Development commands
├── mypy.ini                      # MyPy configuration
├── pyproject.toml               # Poetry configuration and dependencies
└── README.md                    # This file
```

## Setup Instructions

### Prerequisites

- **Python 3.12+**: Install from [python.org](https://python.org)
- **Poetry**: Install from [python-poetry.org](https://python-poetry.org)
- **Docker & Docker Compose**: For containerized development
- **PostgreSQL**: For local database (optional with Docker)

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd usersnack
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Environment variables** (`.env` file):
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=password
   DB_NAME=usersnack

   # Application Configuration
   DEBUG=true
   LOG_LEVEL=INFO
   ```

### Database Configuration

#### Option 1: Docker Compose (Recommended)
```bash
# Start PostgreSQL and application
docker-compose -f docker/docker-compose.yml up -d

# Run migrations
poetry run alembic upgrade head
```

#### Option 2: Local PostgreSQL
```bash
# Install and start PostgreSQL locally
# Create database
createdb usersnack

# Run migrations
poetry run alembic upgrade head
```

### Running the Application

#### Development Mode
```bash
# Using Poetry
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Using Make
make dev
```

#### Production Mode
```bash
# Using Docker
docker-compose -f docker/docker-compose.yml up

# Using Poetry
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Data Seeding

The application automatically seeds the database with sample data on startup. To manually seed:

```bash
# Seed with sample pizzas and extras
poetry run python -c "
import asyncio
from scripts.seed import seed_db
from app.db.session import get_session_maker
from app.db.uow import UnitOfWork

async def main():
    session_maker = get_session_maker()
    async with session_maker() as session:
        uow = UnitOfWork(session)
        async with uow:
            await seed_db(uow)

asyncio.run(main())
"
```

### API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing Documentation

### Test Structure

The test suite is organized into multiple layers:

- **Unit Tests** ([`tests/unit/`](tests/unit/)): Test individual components in isolation
- **E2E Tests** ([`tests/e2e/`](tests/e2e/)): Test complete API workflows
- **Integration Tests**: Test database interactions with real PostgreSQL

### Testing Technologies

- **Pytest**: Primary testing framework with async support
- **Pytest-mock**: Mocking and stubbing for unit tests
- **Testcontainers**: Real PostgreSQL instances for integration tests
- **HTTPX**: Async HTTP client for API testing
- **Factory Functions**: Test data generation utilities

### Test Configuration

The [`tests/conftest.py`](tests/conftest.py) file provides:

- **Database Setup**: Automatic PostgreSQL container management
- **Test Fixtures**: Pre-configured test data and mocks
- **Factory Functions**: Dynamic test data creation
- **Migration Management**: Automatic schema setup for tests

### Running Tests

#### All Tests
```bash
# Using Poetry
poetry run pytest

# Using Make
make test
```

#### Unit Tests Only
```bash
poetry run pytest tests/unit/ -v
```

#### E2E Tests Only
```bash
poetry run pytest tests/e2e/ -v
```

#### With Coverage
```bash
poetry run pytest --cov=app --cov-report=html
```

#### Specific Test File
```bash
poetry run pytest tests/unit/test_cart_service.py -v
```

### Test Requirements and Dependencies

Test-specific dependencies are managed in the `[tool.poetry.group.dev.dependencies]` section:

- `pytest ^8.0.0`: Core testing framework
- `pytest-asyncio ^0.23.0`: Async test support
- `httpx ^0.26.0`: HTTP client for API tests
- `testcontainers-postgres ^0.0.1a5`: PostgreSQL containers for integration tests

### Writing Tests

#### Unit Test Example
```python
# tests/unit/test_cart_service.py
import pytest
from unittest.mock import AsyncMock
from app.services.cart_service import CartService

@pytest.mark.asyncio
async def test_add_to_cart(mock_uow, sample_pizza, sample_extra):
    # Setup mocks
    mock_uow.pizzas.get = AsyncMock(return_value=sample_pizza)
    mock_uow.extras.get = AsyncMock(return_value=sample_extra)
    
    # Test the service
    cart_service = CartService(mock_uow, mock_order_service)
    result = await cart_service.add_to_cart(cart_item_in, "test_cart")
    
    # Assertions
    assert result.subtotal > 0
    mock_uow.carts.add_item.assert_called_once()
```

#### E2E Test Example
```python
# tests/e2e/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_cart_and_checkout(client: AsyncClient):
    # Add item to cart
    response = await client.post("/api/carts/items", json={
        "pizza_id": str(pizza_id),
        "quantity": 2,
        "extras": []
    }, headers={"X-Cart-Token": "test-cart"})
    
    assert response.status_code == 200
    
    # Checkout cart
    checkout_response = await client.post("/api/carts/checkout", json={
        "unique_identifier": "test-cart",
        "fullname": "John Doe",
        "full_address": "123 Test St"
    })
    
    assert checkout_response.status_code == 200
```

## API Endpoints

### Health Check
- `GET /health` - Application health status

### Pizza Catalog
- `GET /api/pizzas` - List all pizzas with pagination
- `GET /api/pizzas/{pizza_id}` - Get specific pizza details

### Extras Catalog
- `GET /api/extras` - List all available extras

### Cart Management
- `POST /api/carts/items` - Add item to cart
- `GET /api/carts` - Get cart contents with calculated totals
- `PUT /api/carts/items/{item_id}` - Update cart item quantity
- `DELETE /api/carts/items/{item_id}` - Remove item from cart
- `DELETE /api/carts` - Clear entire cart
- `POST /api/carts/checkout` - Convert cart to order

### Order Management
- `POST /api/orders` - Create order directly (bypass cart)
- `GET /api/orders/{order_id}` - Get order details
- `POST /api/orders/quote` - Get price quote without creating order

### Request Headers

Cart operations require one of these headers for identification:
- `X-Cart-Token: <uuid>` - Anonymous cart identification
- `X-Cart-Email: <email>` - Email-based cart identification

### Response Format

All API responses follow a consistent envelope format:

```json
{
  "success": true,
  "data": { /* endpoint-specific data */ },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-01T00:00:00Z",
    "page": 1,
    "size": 20,
    "total": 100
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "validation_error",
    "title": "Validation failed",
    "detail": "Detailed error message",
    "field_errors": { "field": ["error message"] }
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2025-01-01T00:00:00Z"
  }
}
```

## Database Schema

### Core Entities

#### Pizza
- `id` (UUID, PK): Unique identifier
- `name` (String): Pizza name (unique)
- `base_price` (Numeric): Base price in decimal format
- `image_url` (Text): URL to pizza image
- `ingredients` (Array): List of ingredients
- `is_active` (Boolean): Availability status
- `created_at`, `updated_at` (Timestamp): Audit fields

#### Extra
- `id` (UUID, PK): Unique identifier
- `name` (String): Extra name (unique)
- `price` (Numeric): Extra price in decimal format
- `is_active` (Boolean): Availability status
- `created_at`, `updated_at` (Timestamp): Audit fields

#### Cart
- `id` (UUID, PK): Unique identifier
- `uniqueIdentifier` (String): Cart identification (email or token)
- `created_at`, `updated_at` (Timestamp): Audit fields

#### CartItem
- `id` (UUID, PK): Unique identifier
- `cart_id` (UUID, FK): Reference to cart
- `pizza_id` (UUID): Reference to pizza
- `quantity` (Integer): Item quantity
- `selected_extras` (JSON): Selected extra IDs
- `created_at`, `updated_at` (Timestamp): Audit fields

#### CustomerInfo
- `id` (UUID, PK): Unique identifier
- `uniqueIdentifier` (String): Customer identification
- `fullname` (String): Customer full name
- `full_address` (Text): Complete address
- `created_at`, `updated_at` (Timestamp): Audit fields

#### Order
- `id` (UUID, PK): Unique identifier
- `uniqueIdentifier` (String): Order identification
- `status` (String): Order status
- `subtotal` (Numeric): Order subtotal
- `extras_total` (Numeric): Total extras cost
- `grand_total` (Numeric): Final total
- `customer_id` (UUID, FK): Reference to customer
- `created_at`, `updated_at` (Timestamp): Audit fields

#### OrderItem
- `id` (UUID, PK): Unique identifier
- `order_id` (UUID, FK): Reference to order
- `pizza_id` (UUID): Reference to pizza
- `quantity` (Integer): Item quantity
- `selected_extras` (JSON): Selected extra IDs
- `unit_base_price` (Numeric): Pizza price at order time
- `unit_extras_total` (Numeric): Extras total at order time
- `line_total` (Numeric): Line item total
- `created_at`, `updated_at` (Timestamp): Audit fields

### Database Indexes

- `pizzas(is_active)` - Fast filtering of active pizzas
- `extras(is_active)` - Fast filtering of active extras
- `carts(uniqueIdentifier)` - Unique cart identification
- `customer_info(uniqueIdentifier)` - Unique customer identification
- `orders(customer_id)` - Customer order history
- `cart_items(cart_id)` - Cart item lookup
- `order_items(order_id)` - Order item lookup

## Configuration

### Environment Variables

The application uses environment-based configuration managed by Pydantic Settings:

```python
# app/core/config.py
class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "usersnack"
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
```

### Development Commands

The [`Makefile`](Makefile) provides convenient development commands:

```bash
make dev          # Start development server
make test         # Run all tests
make lint         # Run linting
make format       # Format code
make type-check   # Run type checking
make migrate      # Run database migrations
make seed         # Seed database with sample data
```

### Docker Configuration

#### Development
```bash
# Start all services
docker-compose -f docker/docker-compose.yml up

# Start in background
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f app
```

#### Production Build
```bash
# Build production image
docker build -f docker/Dockerfile -t usersnack-api .

# Run production container
docker run -p 8000:8000 --env-file .env usersnack-api
```

---

## Getting Started

1. **Quick Start with Docker**:
   ```bash
   cp .env.example .env
   docker-compose -f docker/docker-compose.yml up
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

3. **Run Tests**:
   ```bash
   poetry install
   poetry run pytest
   ```

4. **Explore the API**:
   - Browse pizzas: `GET /api/pizzas`
   - Add to cart: `POST /api/carts/items`
   - Checkout: `POST /api/carts/checkout`

For detailed API usage examples, visit the interactive documentation at `/docs` when the application is running.