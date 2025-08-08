import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.limiter import limiter
from app.core.response import Response, ok
from app.db.session import get_session_maker
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.schemas.cart import CartItemIn, CartOut
from app.services.cart_service import CartService
from app.core.config import get_settings
from app.api.deps import get_cart_service

router = APIRouter()


@router.post("/items", response_model=Response[CartOut])
@limiter.limit("10/minute")
async def add_to_cart(
    request: Request,
    item_in: CartItemIn,
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(get_cart_service),
):
    cart = await cart_service.add_to_cart(item_in, x_cart_email, x_cart_token)
    return ok(cart)


@router.get("/", response_model=Response[CartOut])
async def get_cart(
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(get_cart_service),
):
    cart = await cart_service.get_cart_details(x_cart_email, x_cart_token)
    return ok(cart)
