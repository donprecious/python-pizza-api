import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Cart, CartItem


class CartRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[Cart]:
        result = await self.session.execute(select(Cart).where(Cart.email == email))
        return result.scalars().first()

    async def get_by_token(self, token: uuid.UUID) -> Optional[Cart]:
        result = await self.session.execute(select(Cart).where(Cart.cart_token == token))
        return result.scalars().first()

    async def create(
        self, email: Optional[str] = None, token: Optional[uuid.UUID] = None
    ) -> Cart:
        cart = Cart(email=email, cart_token=token)
        self.session.add(cart)
        await self.session.commit()
        return cart

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
