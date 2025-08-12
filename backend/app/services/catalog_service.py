import uuid
from typing import Sequence

from app.core.exceptions import NotFoundAppError
from app.db.models import Extra, Pizza
from app.schemas.pagination import Page, PaginationParams
from app.schemas.catalog import PizzaOut
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.pizza_repo import PizzaRepo


from app.db.uow import UOWDep


class CatalogService:
    def __init__(self, uow: UOWDep) -> None:
        self._uow = uow

    async def get_pizza(self, pizza_id: uuid.UUID) -> Pizza:
        async with self._uow:
            pizza = await self._uow.pizzas.get(pizza_id)
            if not pizza:
                raise NotFoundAppError(f"Pizza with id {pizza_id} not found")
            return pizza

    async def list_pizzas(
        self,
        search: str | None = None,
        ingredients: list[str] | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Page[PizzaOut]:
        async with self._uow:
            pizzas, total = await self._uow.pizzas.get_all(
                search=search,
                ingredients=ingredients,
                min_price=min_price,
                max_price=max_price,
                page=page,
                page_size=page_size,
            )
            params = PaginationParams(page=page, per_page=page_size)
            return Page(
                items=[PizzaOut.from_orm(p) for p in pizzas],
                meta=params.build_meta(total),
            )

    async def list_extras(self) -> Sequence[Extra]:
        return await self._uow.extras.get_all()
