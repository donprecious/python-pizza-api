import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Cart, CartItem


class CartRepo:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[Cart]:
        async with self.session() as session:
            result = await session.execute(select(Cart).where(Cart.email == email))
            return result.scalars().first()

    async def get_by_token(self, token: uuid.UUID) -> Optional[Cart]:
        async with self.session() as session:
            result = await session.execute(select(Cart).where(Cart.cart_token == token))
            return result.scalars().first()

    async def create(
        self, email: Optional[str] = None, token: Optional[uuid.UUID] = None
    ) -> Cart:
        async with self.session() as session:
            cart = Cart(email=email, cart_token=token)
            session.add(cart)
            await session.commit()
            return cart

    async def add_item(self, item: CartItem) -> CartItem:
        async with self.session() as session:
            session.add(item)
            await session.commit()
            return item

    async def get_item(self, item_id: uuid.UUID) -> Optional[CartItem]:
        async with self.session() as session:
            return await session.get(CartItem, item_id)

    async def delete_item(self, item: CartItem):
        async with self.session() as session:
            await session.delete(item)
            await session.commit()

    async def clear(self, cart: Cart):
        async with self.session() as session:
            for item in cart.items:
                await session.delete(item)
            await session.commit()
