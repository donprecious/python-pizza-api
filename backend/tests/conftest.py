import asyncio
import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, AsyncMock

import pytest
from alembic import command
from alembic.config import Config
from testcontainers.postgres import PostgresContainer
from app.core.config import Settings, get_settings
from app.db.session import get_session_maker
from app.db.models import Pizza, Extra, Cart, CartItem, CustomerInfo, Order, OrderItem
from app.db.uow import UnitOfWork
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


# ============================================================================
# PYTEST-MOCK FIXTURES AND TEST DATA FACTORIES FOR UNIT TESTS
# ============================================================================

@pytest.fixture
def mock_uow():
    """Mock UnitOfWork for unit testing"""
    uow = Mock(spec=UnitOfWork)
    uow.cart_repo = Mock()
    uow.pizza_repo = Mock()
    uow.extra_repo = Mock()
    uow.customer_repo = Mock()
    uow.order_repo = Mock()
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    return uow


# ============================================================================
# MODEL FIXTURES AND FACTORIES
# ============================================================================

@pytest.fixture
def sample_pizza():
    """Sample Pizza model instance"""
    return Pizza(
        id=uuid.uuid4(),
        name="Margherita",
        base_price=Decimal("12.99"),
        image_url="https://example.com/margherita.jpg",
        ingredients=["tomato sauce", "mozzarella", "basil"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_extra():
    """Sample Extra model instance"""
    return Extra(
        id=uuid.uuid4(),
        name="Extra Cheese",
        price=Decimal("2.50"),
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_customer():
    """Sample CustomerInfo model instance"""
    return CustomerInfo(
        id=uuid.uuid4(),
        uniqueIdentifier="customer_123",
        fullname="John Doe",
        full_address="123 Main St, City, State 12345",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_cart():
    """Sample Cart model instance"""
    return Cart(
        id=uuid.uuid4(),
        uniqueIdentifier="cart_123",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_cart_item(sample_cart, sample_pizza):
    """Sample CartItem model instance"""
    return CartItem(
        id=uuid.uuid4(),
        cart_id=sample_cart.id,
        pizza_id=sample_pizza.id,
        quantity=2,
        selected_extras={"extra_cheese": 1, "pepperoni": 1},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_order(sample_customer):
    """Sample Order model instance"""
    return Order(
        id=uuid.uuid4(),
        uniqueIdentifier="order_123",
        status="pending",
        subtotal=Decimal("25.98"),
        extras_total=Decimal("5.00"),
        grand_total=Decimal("30.98"),
        customer_id=sample_customer.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def sample_order_item(sample_order, sample_pizza):
    """Sample OrderItem model instance"""
    return OrderItem(
        id=uuid.uuid4(),
        order_id=sample_order.id,
        pizza_id=sample_pizza.id,
        quantity=2,
        selected_extras={"extra_cheese": 1, "pepperoni": 1},
        unit_base_price=Decimal("12.99"),
        unit_extras_total=Decimal("2.50"),
        line_total=Decimal("30.98"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


# ============================================================================
# FACTORY FUNCTIONS FOR CREATING TEST DATA
# ============================================================================

def create_pizza(**kwargs):
    """Factory function to create Pizza instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "name": "Test Pizza",
        "base_price": Decimal("10.99"),
        "image_url": "https://example.com/test.jpg",
        "ingredients": ["cheese", "tomato"],
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return Pizza(**defaults)


def create_extra(**kwargs):
    """Factory function to create Extra instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "name": "Test Extra",
        "price": Decimal("1.99"),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return Extra(**defaults)


def create_customer(**kwargs):
    """Factory function to create CustomerInfo instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "uniqueIdentifier": f"customer_{uuid.uuid4().hex[:8]}",
        "fullname": "Test Customer",
        "full_address": "123 Test St, Test City, TC 12345",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return CustomerInfo(**defaults)


def create_cart(**kwargs):
    """Factory function to create Cart instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "uniqueIdentifier": f"cart_{uuid.uuid4().hex[:8]}",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return Cart(**defaults)


def create_cart_item(**kwargs):
    """Factory function to create CartItem instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "cart_id": uuid.uuid4(),
        "pizza_id": uuid.uuid4(),
        "quantity": 1,
        "selected_extras": {},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return CartItem(**defaults)


def create_order(**kwargs):
    """Factory function to create Order instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "uniqueIdentifier": f"order_{uuid.uuid4().hex[:8]}",
        "status": "pending",
        "subtotal": Decimal("10.99"),
        "extras_total": Decimal("0.00"),
        "grand_total": Decimal("10.99"),
        "customer_id": uuid.uuid4(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return Order(**defaults)


def create_order_item(**kwargs):
    """Factory function to create OrderItem instances with custom attributes"""
    defaults = {
        "id": uuid.uuid4(),
        "order_id": uuid.uuid4(),
        "pizza_id": uuid.uuid4(),
        "quantity": 1,
        "selected_extras": {},
        "unit_base_price": Decimal("10.99"),
        "unit_extras_total": Decimal("0.00"),
        "line_total": Decimal("10.99"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    defaults.update(kwargs)
    return OrderItem(**defaults)
