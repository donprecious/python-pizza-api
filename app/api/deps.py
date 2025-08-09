from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.customer_repo import CustomerRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.order_repo import OrderRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.db.session import get_db_session
from app.services.cart_service import CartService
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService


from app.db.uow import UnitOfWork


def get_uow(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UnitOfWork:
    return UnitOfWork(session)


def get_catalog_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> CatalogService:
    return CatalogService(uow)


def get_order_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> OrderService:
    return OrderService(uow)


def get_cart_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> CartService:
    return CartService(uow, order_service)