import uuid
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, Request

from app.containers import Container
from app.core.limiter import limiter
from app.core.response import ok
from app.schemas.cart import CartItemIn, CartOut
from app.services.cart_service import CartService

router = APIRouter()


@router.post("/items", response_model=CartOut)
@limiter.limit("10/minute")
@inject
async def add_to_cart(
    request: Request,
    item_in: CartItemIn,
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(Provide[Container.cart_service]),
):
    cart = await cart_service.add_to_cart(item_in, x_cart_email, x_cart_token)
    return ok(cart)


@router.get("/", response_model=CartOut)
@inject
async def get_cart(
    x_cart_email: Optional[str] = Header(None),
    x_cart_token: Optional[uuid.UUID] = Header(None),
    cart_service: CartService = Depends(Provide[Container.cart_service]),
):
    cart = await cart_service.get_cart_details(x_cart_email, x_cart_token)
    return ok(cart)
