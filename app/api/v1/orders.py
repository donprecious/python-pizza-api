import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.containers import Container
from app.core.limiter import limiter
from app.core.response import ok
from app.schemas.order import OrderIn, OrderOut, QuoteOut
from app.services.order_service import OrderService

router = APIRouter()


@router.post("/", response_model=OrderOut)
@limiter.limit("5/minute")
@inject
async def create_order(
    request: Request,
    order_in: OrderIn,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    order = await order_service.create_order(order_in)
    return ok(order)


@router.post(":quote", response_model=QuoteOut)
@inject
async def quote_order(
    order_in: OrderIn,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    # This is not ideal, but for the MVP we'll create and then discard
    order = await order_service.create_order(order_in)
    return ok(order)


@router.get("/{order_id}", response_model=OrderOut)
@inject
async def get_order(
    order_id: uuid.UUID,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    order = await order_service.get_order(order_id)
    return ok(order)
