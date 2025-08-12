import asyncio
import json
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from alembic import command
from alembic.config import Config

from app.core.config import Settings
from app.db.session import get_db_session
from app.db.uow import UnitOfWork
from app.db.models import Pizza, Extra
from app.db.base import Base
from scripts.seed import seed_data


class E2ETestSettings(Settings):
    """E2E Test-specific settings that override the default configuration."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@pytest.fixture(scope="session")
def e2e_postgres_container():
    """Start a PostgreSQL container for E2E testing."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def e2e_test_settings(e2e_postgres_container: PostgresContainer) -> E2ETestSettings:
    """Create test settings with the container database configuration."""
    return E2ETestSettings(
        DB_HOST=e2e_postgres_container.get_container_host_ip(),
        DB_PORT=e2e_postgres_container.get_exposed_port(5432),
        DB_USER=e2e_postgres_container.POSTGRES_USER,
        DB_PASSWORD=e2e_postgres_container.POSTGRES_PASSWORD,
        DB_NAME=e2e_postgres_container.POSTGRES_DB,
    )


@pytest.fixture(scope="session")
def e2e_test_engine(e2e_test_settings: E2ETestSettings):
    """Create a test database engine for E2E tests."""
    engine = create_async_engine(e2e_test_settings.db_url)
    yield engine


@pytest.fixture(scope="session")
def e2e_test_session_maker(e2e_test_engine):
    """Create a test session maker for E2E tests."""
    return async_sessionmaker(autocommit=False, autoflush=False, bind=e2e_test_engine)


@pytest_asyncio.fixture(scope="session")
async def e2e_create_tables(e2e_test_engine):
    """Create database tables for E2E tests."""
    async with e2e_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return True


@pytest_asyncio.fixture(scope="session")
async def e2e_seed_data(e2e_test_session_maker, e2e_create_tables):
    """Seed the E2E test database with pizza and extra data."""
    # Ensure tables have been created before seeding
    async with e2e_test_session_maker() as session:
        uow = UnitOfWork(session)
        async with uow:
            await seed_test_data(uow)
    return True


async def seed_test_data(uow: UnitOfWork):
    """Seed the test database with pizza and extra data."""
    # Load pizza data
    with open("pizza.json", "r") as f:
        pizzas_data = json.load(f)

    pizzas_to_seed = [
        {
            "name": p["name"],
            "base_price": p["price"],
            "image_url": p["img"],
            "ingredients": p["ingredients"],
        }
        for p in pizzas_data
    ]
    await seed_data(uow, pizzas_to_seed, Pizza, "name")

    # Load extras data
    with open("extras.json", "r") as f:
        extras_data = json.load(f)
    await seed_data(uow, extras_data, Extra, "name")


@pytest_asyncio.fixture(scope="function")
async def e2e_test_session(e2e_test_session_maker, e2e_seed_data) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session for each E2E test."""
    async with e2e_test_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def e2e_test_app(e2e_test_settings: E2ETestSettings, e2e_test_session: AsyncSession) -> FastAPI:
    """Create a test FastAPI application for E2E tests."""
    # Create the app without lifespan (we handle seeding manually)
    app = FastAPI(
        title="Usersnack API (E2E Test)",
        description="A FastAPI backend for a pizza ordering service (E2E Test Environment).",
        version="0.1.0",
    )
    
    # Include all the routers
    from app.api.routers import carts, extras, health, orders, pizzas
    from app.core.exception_handler import add_exception_handlers
    from app.core.limiter import limiter
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    app.include_router(pizzas.router, prefix="/api/pizzas", tags=["pizzas"])
    app.include_router(extras.router, prefix="/api/extras", tags=["extras"])
    app.include_router(carts.router, prefix="/api/carts", tags=["carts"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(health.router, prefix="/health", tags=["health"])
    
    add_exception_handlers(app)
    
    # Override the database session dependency
    async def override_get_db_session():
        yield e2e_test_session
    
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    # Override the settings
    from app.core.config import get_settings
    app.dependency_overrides[get_settings] = lambda: e2e_test_settings
    
    return app


@pytest_asyncio.fixture(scope="function")
async def e2e_test_client(e2e_test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client for E2E tests."""
    async with AsyncClient(app=e2e_test_app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def e2e_test_uow(e2e_test_session: AsyncSession) -> UnitOfWork:
    """Create a test Unit of Work for E2E tests."""
    return UnitOfWork(e2e_test_session)