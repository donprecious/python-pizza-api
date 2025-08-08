import asyncio

import pytest
from alembic import command
from alembic.config import Config
from testcontainers.postgres import PostgresContainer
from app.core.config import Settings, get_settings
from app.db.session import get_session_maker
from main import create_app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def settings(postgres_container: PostgresContainer):
    return Settings(
        DB_HOST=postgres_container.get_container_host_ip(),
        DB_PORT=postgres_container.get_exposed_port(5432),
        DB_USER=postgres_container.POSTGRES_USER,
        DB_PASSWORD=postgres_container.POSTGRES_PASSWORD,
        DB_NAME=postgres_container.POSTGRES_DB,
    )


@pytest.fixture(scope="session", autouse=True)
def run_migrations(settings: Settings):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def app(settings: Settings):
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    return app
