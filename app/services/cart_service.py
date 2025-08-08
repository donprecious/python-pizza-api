import uuid
from typing import Optional

from app.core.errors import InvalidIdentityAppError, NotFoundAppError
from app.db.models import Cart, CartItem
from app.repos.cart_repo import CartRepo
from app.repos.extra_repo import ExtraRepo
from app.repos.pizza_repo import PizzaRepo
from app.schemas.cart import CartItemIn


class CartService:
    def __init__(
        self,
        cart_repo: CartRepo,
        pizza_repo: PizzaRepo,
        extra_repo: ExtraRepo,
    ):
        self.cart_repo = cart_repo
        self.pizza_repo = pizza_repo
        self.extra_repo = extra_repo

    async def _get_cart(
        self, email: Optional[str] = None, token: Optional[uuid.UUID] = None
    ) -> Cart:
        if email:
            cart = await self.cart_repo.get_by_email(email)
        elif token:
            cart = await self.cart_repo.get_by_token(token)
        else:
            raise InvalidIdentityAppError("Either email or token must be provided")

        if not cart:
            cart = await self.cart_repo.create(email=email, token=token)
        return cart

    async def add_to_cart(
        self,
        item_in: CartItemIn,
        email: Optional[str] = None,
        token: Optional[uuid.UUID] = None,
    ) -> Cart:
        cart = await self._get_cart(email, token)
        pizza = await self.pizza_repo.get(item_in.pizza_id)
        if not pizza:
            raise NotFoundAppError(f"Pizza with id {item_in.pizza_id} not found")

        extras = [await self.extra_repo.get(extra_id) for extra_id in item_in.extras]
        if any(e is None for e in extras):
            raise NotFoundAppError("One or more extras not found")

        cart_item = CartItem(
            cart_id=cart.id,
            pizza_id=item_in.pizza_id,
            quantity=item_in.quantity,
            selected_extras=[extra.id for extra in extras if extra],
        )
        await self.cart_repo.add_item(cart_item)
        return cart

    async def get_cart_details(
        self, email: Optional[str] = None, token: Optional[uuid.UUID] = None
    ) -> Cart:
        return await self._get_cart(email, token)
