import uuid
from typing import Sequence

from app.core.exceptions import NotFoundAppError
from app.db.models import Extra, Pizza
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.pizza_repo import PizzaRepo


class CatalogService:
    def __init__(
        self,
        pizza_repo: PizzaRepo,
        extra_repo: ExtraRepo,
    ):
        self._pizza_repo = pizza_repo
        self._extra_repo = extra_repo

    async def get_pizza(self, pizza_id: uuid.UUID) -> Pizza:
        pizza = await self._pizza_repo.get(pizza_id)
        if not pizza:
            raise NotFoundAppError(f"Pizza with id {pizza_id} not found")
        return pizza

    async def list_pizzas(self) -> Sequence[Pizza]:
        return await self._pizza_repo.get_all()

    async def list_extras(self) -> Sequence[Extra]:
        return await self._extra_repo.get_all()
