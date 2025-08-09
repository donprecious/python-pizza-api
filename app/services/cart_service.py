import uuid
from typing import Optional

from decimal import Decimal
from app.core.exceptions import InvalidIdentityAppError, NotFoundAppError
from app.db.models import Cart, CartItem
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.schemas.cart import CartItemIn, CartItemOut, CartOut


class CartService:
    def __init__(
        self,
        cart_repo: CartRepo,
        pizza_repo: PizzaRepo,
        extra_repo: ExtraRepo,
    ):
        self._cart_repo = cart_repo
        self._pizza_repo = pizza_repo
        self._extra_repo = extra_repo

    async def _get_cart(self, unique_identifier: str) -> Cart:
        return await self._cart_repo.find_or_create(unique_identifier)

    async def _calculate_cart_totals(self, cart: Cart) -> CartOut:
        items_out = []
        subtotal = Decimal(0)

        for item in cart.items:
            pizza = await self._pizza_repo.get(item.pizza_id)
            if not pizza:
                raise NotFoundAppError(f"Pizza with id {item.pizza_id} not found")

            extras = await self._extra_repo.get_many(
                [uuid.UUID(str(eid)) for eid in item.selected_extras]
            )
            unit_extras_total = sum(Decimal(str(extra.price)) for extra in extras)
            unit_price = Decimal(str(pizza.base_price)) + unit_extras_total
            total_price = unit_price * item.quantity

            items_out.append(
                CartItemOut(
                    id=item.id,
                    pizza_id=item.pizza_id,
                    quantity=item.quantity,
                    extras=[extra.id for extra in extras],
                    unit_price=float(unit_price),
                    total_price=float(total_price),
                )
            )
            subtotal += total_price

        return CartOut(
            id=cart.id,
            unique_identifier=cart.uniqueIdentifier,
            items=items_out,
            subtotal=float(subtotal),
            grand_total=float(subtotal),  # Assuming no additional charges for now
        )

    async def add_to_cart(
        self,
        item_in: CartItemIn,
        unique_identifier: str,
    ) -> CartOut:
        ''' add pizza to cart, even if the pizza already exists, we can add it as a new item, because the extras can be different, we just keep it flexible'''
        cart = await self._get_cart(unique_identifier)
        pizza = await self._pizza_repo.get(item_in.pizza_id)
        if not pizza:
            raise NotFoundAppError(f"Pizza with id {item_in.pizza_id} not found")

        extras = [await self._extra_repo.get(extra_id) for extra_id in item_in.extras]
        if any(e is None for e in extras):
            raise NotFoundAppError("One or more extras not found")

        cart_item = CartItem(
            cart_id=cart.id,
            pizza_id=item_in.pizza_id,
            quantity=item_in.quantity,
            selected_extras=[str(extra.id) for extra in extras if extra],
        )
        await self._cart_repo.add_item(cart_item)
        cart = await self._get_cart(unique_identifier)
        return await self._calculate_cart_totals(cart)

    async def get_cart_details(self, unique_identifier: str) -> CartOut:
        cart = await self._get_cart(unique_identifier)
        return await self._calculate_cart_totals(cart)
