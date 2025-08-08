import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Order


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, order_id: uuid.UUID) -> Optional[Order]:
        return await self.session.get(Order, order_id)

    async def create(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        return order
