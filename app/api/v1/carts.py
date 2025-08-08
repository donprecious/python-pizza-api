import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.limiter import limiter
from app.core.response import ok
from app.db.session import get_session_maker
from app.repos.cart_repo import CartRepo
from app.repos.pizza_repo import PizzaRepo
from app.repos.extra_repo import ExtraRepo
from app.schemas.cart import CartItemIn, CartOut
from app.services.cart_service import CartService
from app.core.config import get_settings

router = APIRouter()


async def get_db() -> AsyncSession:
    session_maker = get_session_maker(get_settings())
    async with session_maker() as session:
        yield session


def get_cart_repo(db: AsyncSession = Depends(get_db)) -> CartRepo:
    return CartRepo(db)


def get_pizza_repo(db: AsyncSession = Depends(get_db)) -> PizzaRepo:
    return PizzaRepo(db)


def get_extra_repo(db: AsyncSession = Depends(get_db)) -> ExtraRepo:
    return ExtraRepo(db)


def get_cart_service(
    cart_repo: CartRepo = Depends(get_cart_repo),
    pizza_repo: PizzaRepo = Depends(get_pizza_repo),
    extra_repo: ExtraRepo = Depends(get_extra_repo)
) -> CartService:
    return CartService(cart_repo=cart_repo, pizza_repo=pizza_repo, extra_repo=extra_repo)


@router.post("/items", response_model=CartOut)
@limiter.limit("10/minute")
async def add_to_cart(
    request: Request,
    item_in: CartItemIn,
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(get_cart_service),
):
    cart = await cart_service.add_to_cart(item_in, x_cart_email, x_cart_token)
    return cart


@router.get("/", response_model=CartOut)
async def get_cart(
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(get_cart_service),
):
    cart = await cart_service.get_cart_details(x_cart_email, x_cart_token)
    return cart
