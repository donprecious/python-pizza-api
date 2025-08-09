import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Cart, CartItem


class CartRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_unique_identifier(self, unique_identifier: str) -> Optional[Cart]:
        result = await self.session.execute(
            select(Cart)
            .where(Cart.uniqueIdentifier == unique_identifier)
            .options(selectinload(Cart.items))
        )
        return result.scalars().first()

    async def create(self, unique_identifier: str) -> Cart:
        cart = Cart(uniqueIdentifier=unique_identifier)
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def find_or_create(self, unique_identifier: str) -> Cart:
        """Find existing cart by uniqueIdentifier or create a new one."""
        existing_cart = await self.get_by_unique_identifier(unique_identifier)
        if existing_cart:
            return existing_cart
        return await self.create(unique_identifier)

    async def add_item(self, item: CartItem) -> CartItem:
        self.session.add(item)
        await self.session.commit()
        return item

    async def get_item(self, item_id: uuid.UUID) -> Optional[CartItem]:
        return await self.session.get(CartItem, item_id)

    async def delete_item(self, item: CartItem):
        await self.session.delete(item)
        await self.session.commit()

    async def clear(self, cart: Cart):
        for item in cart.items:
            await self.session.delete(item)
        await self.session.commit()
