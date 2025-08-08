import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.limiter import limiter
from app.core.response import ok
from app.db.session import get_session_maker
from app.repos.cart_repo import CartRepo
from app.repos.order_repo import OrderRepo
from app.schemas.order import OrderIn, OrderOut, QuoteOut
from app.services.order_service import OrderService
from app.core.config import get_settings

router = APIRouter()


async def get_db() -> AsyncSession:
    session_maker = get_session_maker(get_settings())
    async with session_maker() as session:
        yield session


def get_order_repo(db: AsyncSession = Depends(get_db)) -> OrderRepo:
    return OrderRepo(db)


def get_cart_repo(db: AsyncSession = Depends(get_db)) -> CartRepo:
    return CartRepo(db)


def get_order_service(
    order_repo: OrderRepo = Depends(get_order_repo),
    cart_repo: CartRepo = Depends(get_cart_repo)
) -> OrderService:
    return OrderService(order_repo=order_repo, cart_repo=cart_repo)


@router.post("/", response_model=OrderOut)
@limiter.limit("5/minute")
async def create_order(
    request: Request,
    order_in: OrderIn,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.create_order(order_in)
    return order


@router.post(":quote", response_model=QuoteOut)
async def quote_order(
    order_in: OrderIn,
    order_service: OrderService = Depends(get_order_service),
):
    # This is not ideal, but for the MVP we'll create and then discard
    order = await order_service.create_order(order_in)
    return order


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: uuid.UUID,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order(order_id)
    return order
