import uuid
from typing import List
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import Response, ok
from app.schemas.catalog import PizzaOut
from app.schemas.pagination import Page
from app.services.catalog_service import CatalogService
from app.api.deps import get_catalog_service

router = APIRouter()


@router.get("/", response_model=Response[Page[PizzaOut]])
async def list_pizzas(
    search: str | None = None,
    ingredients: Annotated[list[str] | None, Query()] = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = 1,
    page_size: int = 10,
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    pizzas = await catalog_service.list_pizzas(
        search=search,
        ingredients=ingredients,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )
    return ok(pizzas)


