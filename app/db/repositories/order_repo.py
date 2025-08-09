import uuid
from typing import Optional, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Order


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, order_id: uuid.UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items), selectinload(Order.customer))
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_unique_identifier(self, unique_identifier: str) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.uniqueIdentifier == unique_identifier)
            .options(selectinload(Order.items), selectinload(Order.customer))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(self, unique_identifier: Optional[str] = None) -> int:
        stmt = select(func.count()).select_from(Order)
        if unique_identifier:
            stmt = stmt.where(Order.uniqueIdentifier == unique_identifier)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def create(self, order: Order) -> Order:
        self._session.add(order)
        await self._session.flush()
        await self._session.refresh(order, attribute_names=["items", "customer"])
        return order

    async def get_all(
        self,
        unique_identifier: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Order]:
        stmt = select(Order).options(
            selectinload(Order.items), selectinload(Order.customer)
        )
        if unique_identifier:
            stmt = stmt.where(Order.uniqueIdentifier == unique_identifier)
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
