import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Pizza


class PizzaRepo:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def get(self, pizza_id: uuid.UUID) -> Pizza | None:
        async with self.session() as session:
            return await session.get(Pizza, pizza_id)

    async def get_all(self) -> Sequence[Pizza]:
        async with self.session() as session:
            result = await session.execute(select(Pizza).where(Pizza.is_active))
            return result.scalars().all()
