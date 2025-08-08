import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Extra


class ExtraRepo:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def get(self, extra_id: uuid.UUID) -> Extra | None:
        async with self.session() as session:
            return await session.get(Extra, extra_id)

    async def get_all(self) -> Sequence[Extra]:
        async with self.session() as session:
            result = await session.execute(select(Extra).where(Extra.is_active))
            return result.scalars().all()
