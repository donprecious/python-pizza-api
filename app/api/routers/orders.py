import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.limiter import limiter
from app.core.response import Response, ok
from app.db.session import get_session_maker
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.order_repo import OrderRepo
from app.schemas.order import OrderIn, OrderOut, QuoteOut
from app.services.order_service import OrderService
from app.core.config import get_settings
from app.api.deps import get_order_service

router = APIRouter()


@router.post("/", response_model=Response[OrderOut])
@limiter.limit("5/minute")
async def create_order(
    request: Request,
    order_in: OrderIn,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.create_order(order_in)
    return ok(order)


@router.post(":quote", response_model=Response[QuoteOut])
async def quote_order(
    order_in: OrderIn,
    order_service: OrderService = Depends(get_order_service),
):
    # This is not ideal, but for the MVP we'll create and then discard
    order = await order_service.create_order(order_in)
    return ok(order)


@router.get("/{order_id}", response_model=Response[OrderOut])
async def get_order(
    order_id: uuid.UUID,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order(order_id)
    return ok(order)
