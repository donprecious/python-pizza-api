from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.config import get_settings
from app.db.session import get_session_maker
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.order_repo import OrderRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.services.cart_service import CartService
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker(get_settings())
    async with session_maker() as session:
        yield session


def get_pizza_repo(db: AsyncSession = Depends(get_db)) -> PizzaRepo:
    return PizzaRepo(db)


def get_extra_repo(db: AsyncSession = Depends(get_db)) -> ExtraRepo:
    return ExtraRepo(db)


def get_cart_repo(db: AsyncSession = Depends(get_db)) -> CartRepo:
    return CartRepo(db)


def get_order_repo(db: AsyncSession = Depends(get_db)) -> OrderRepo:
    return OrderRepo(db)


def get_catalog_service(
    pizza_repo: PizzaRepo = Depends(get_pizza_repo),
    extra_repo: ExtraRepo = Depends(get_extra_repo),
) -> CatalogService:
    return CatalogService(pizza_repo=pizza_repo, extra_repo=extra_repo)


def get_cart_service(
    cart_repo: CartRepo = Depends(get_cart_repo),
    pizza_repo: PizzaRepo = Depends(get_pizza_repo),
    extra_repo: ExtraRepo = Depends(get_extra_repo),
) -> CartService:
    return CartService(cart_repo=cart_repo, pizza_repo=pizza_repo, extra_repo=extra_repo)


def get_order_service(
    order_repo: OrderRepo = Depends(get_order_repo),
    cart_repo: CartRepo = Depends(get_cart_repo),
) -> OrderService:
    return OrderService(order_repo=order_repo, cart_repo=cart_repo)