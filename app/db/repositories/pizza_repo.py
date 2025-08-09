import uuid
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Pizza


class PizzaRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, pizza_id: uuid.UUID) -> Pizza | None:
        return await self._session.get(Pizza, pizza_id)

    async def get_all(
        self,
        search: str | None = None,
        ingredients: list[str] | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[Sequence[Pizza], int]:
        query = select(Pizza).where(Pizza.is_active)
        if search:
            query = query.where(Pizza.name.ilike(f"%{search}%"))
        if ingredients:
            query = query.where(Pizza.ingredients.op("@>")(ingredients))
        if min_price:
            query = query.where(Pizza.base_price >= min_price)
        if max_price:
            query = query.where(Pizza.base_price <= max_price)

        total_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(total_query) or 0

        query = query.limit(page_size).offset((page - 1) * page_size)
        result = await self._session.execute(query)
        return result.scalars().all(), total
