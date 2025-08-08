from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import Response, ok
from app.schemas.catalog import ExtraOut
from app.services.catalog_service import CatalogService
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.api.deps import get_db, get_catalog_service

router = APIRouter()


@router.get("/", response_model=Response[List[ExtraOut]])
async def list_extras(
    catalog_service: CatalogService = Depends(get_catalog_service),
):
    extras = await catalog_service.list_extras()
    return ok(extras)

@router.get("/boom")
def cause_error():
    raise RuntimeError("Something went wrong!")