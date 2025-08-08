import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Order


class OrderRepo:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def get(self, order_id: uuid.UUID) -> Optional[Order]:
        async with self.session() as session:
            return await session.get(Order, order_id)

    async def create(self, order: Order) -> Order:
        async with self.session() as session:
            session.add(order)
            await session.commit()
            return order
