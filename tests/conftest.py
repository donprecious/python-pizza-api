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


@pytest.fixture(scope="session")
def session(settings: Settings):
    Session = get_session_maker()
    return Session()


@pytest.fixture(scope="session", autouse=True)
async def seed_data(session):
    import json
    from app.db.models import Extra, Pizza
    from scripts.seed import seed_data as seed_data_func

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
    await seed_data_func(session, pizzas_to_seed, Pizza, "name")

    with open("extras.json", "r") as f:
        extras_data = json.load(f)
    await seed_data_func(session, extras_data, Extra, "name")
