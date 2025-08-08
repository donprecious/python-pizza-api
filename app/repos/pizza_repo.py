import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Pizza


class PizzaRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, pizza_id: uuid.UUID) -> Pizza | None:
        return await self.session.get(Pizza, pizza_id)

    async def get_all(self) -> Sequence[Pizza]:
        result = await self.session.execute(select(Pizza).where(Pizza.is_active))
        return result.scalars().all()
