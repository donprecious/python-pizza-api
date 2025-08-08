import uuid
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import Container
from app.core.response import ok
from app.schemas.catalog import PizzaOut
from app.services.catalog_service import CatalogService

router = APIRouter()


@router.get("/", response_model=List[PizzaOut])
@inject
async def list_pizzas(
    catalog_service: CatalogService = Depends(Provide[Container.catalog_service]),
):
    pizzas = await catalog_service.list_pizzas()
    return ok(pizzas)


@router.get("/{pizza_id}", response_model=PizzaOut)
@inject
async def get_pizza(
    pizza_id: uuid.UUID,
    catalog_service: CatalogService = Depends(Provide[Container.catalog_service]),
):
    pizza = await catalog_service.get_pizza(pizza_id)
    return ok(pizza)
