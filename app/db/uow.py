from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.customer_repo import CustomerRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.order_repo import OrderRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.db.session import get_db_session


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def pizzas(self) -> PizzaRepo:
        return PizzaRepo(self._session)

    @property
    def extras(self) -> ExtraRepo:
        return ExtraRepo(self._session)

    @property
    def customers(self) -> CustomerRepo:
        return CustomerRepo(self._session)

    @property
    def carts(self) -> CartRepo:
        return CartRepo(self._session)

    @property
    def orders(self) -> OrderRepo:
        return OrderRepo(self._session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


UOWDep = Annotated[UnitOfWork, Depends()]