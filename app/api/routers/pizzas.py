import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import Response, ok
from app.schemas.catalog import PizzaOut
from app.services.catalog_service import CatalogService
from app.api.deps import get_catalog_service

router = APIRouter()


@router.get("/", response_model=Response[List[PizzaOut]])
async def list_pizzas(
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    pizzas = await catalog_service.list_pizzas()
    return ok(pizzas)


@router.get("/{pizza_id}", response_model=Response[PizzaOut])
async def get_pizza(
    pizza_id: uuid.UUID,
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    pizza = await catalog_service.get_pizza(pizza_id)
    return ok(pizza)
