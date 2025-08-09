import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Order


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, order_id: uuid.UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items), selectinload(Order.customer))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_unique_identifier(self, unique_identifier: str) -> List[Order]:
        stmt = (
            select(Order)
            .where(Order.uniqueIdentifier == unique_identifier)
            .options(selectinload(Order.items), selectinload(Order.customer))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order, attribute_names=["items", "customer"])
        print(order)
        print(order.items)
        return order
