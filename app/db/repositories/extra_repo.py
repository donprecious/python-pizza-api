import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Extra


class ExtraRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, extra_id: uuid.UUID) -> Extra | None:
        return await self.session.get(Extra, extra_id)

    async def get_all(self) -> Sequence[Extra]:
        result = await self.session.execute(select(Extra).where(Extra.is_active))
        return result.scalars().all()

    async def get_many(self, extra_ids: list[uuid.UUID]) -> Sequence[Extra]:
        result = await self.session.execute(
            select(Extra).where(Extra.id.in_(extra_ids))
        )
        return result.scalars().all()
