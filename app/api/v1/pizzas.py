import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import ok
from app.schemas.catalog import PizzaOut
from app.services.catalog_service import CatalogService
from app.db.session import get_session_maker
from app.repos.pizza_repo import PizzaRepo
from app.repos.extra_repo import ExtraRepo
from app.core.config import get_settings

router = APIRouter()


async def get_db() -> AsyncSession:
    session_maker = get_session_maker(get_settings())
    async with session_maker() as session:
        yield session


def get_pizza_repo(db: AsyncSession = Depends(get_db)) -> PizzaRepo:
    return PizzaRepo(db)


def get_extra_repo(db: AsyncSession = Depends(get_db)) -> ExtraRepo:
    return ExtraRepo(db)


def get_catalog_service(
    pizza_repo: PizzaRepo = Depends(get_pizza_repo),
    extra_repo: ExtraRepo = Depends(get_extra_repo)
) -> CatalogService:
    return CatalogService(pizza_repo=pizza_repo, extra_repo=extra_repo)


@router.get("/", response_model=List[PizzaOut])
async def list_pizzas(
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    pizzas = await catalog_service.list_pizzas()
    return pizzas


@router.get("/{pizza_id}", response_model=PizzaOut)
async def get_pizza(
    pizza_id: uuid.UUID,
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    pizza = await catalog_service.get_pizza(pizza_id)
    return pizza
