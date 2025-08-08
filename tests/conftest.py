import asyncio

import pytest
from alembic import command
from alembic.config import Config
from testcontainers.postgres import PostgresContainer
from app.containers import Container
from app.core.config import Settings


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
def app_container(postgres_container: PostgresContainer):
    container = Container()
    container.config.override(
        Settings(
            DB_HOST=postgres_container.get_container_host_ip(),
            DB_PORT=postgres_container.get_exposed_port(5432),
            DB_USER=postgres_container.username,
            DB_PASSWORD=postgres_container.password,
            DB_NAME=postgres_container.dbname,
        )
    )
    return container


@pytest.fixture(scope="session", autouse=True)
def run_migrations(app_container: Container):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", app_container.config().db_url)
    command.upgrade(alembic_cfg, "head")
