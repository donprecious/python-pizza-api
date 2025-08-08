from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import Container
from app.core.response import ok
from app.schemas.catalog import ExtraOut
from app.services.catalog_service import CatalogService

router = APIRouter()


@router.get("/", response_model=List[ExtraOut])
@inject
async def list_extras(
    catalog_service: CatalogService = Depends(Provide[Container.catalog_service]),
):
    extras = await catalog_service.list_extras()
    return ok(extras)
