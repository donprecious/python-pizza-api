import asyncio
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from app.db.models import Extra, Pizza
from app.db.session import get_session_maker


async def seed_data(session: AsyncSession, data: list, model, name_field: str):
    """
    Seeds the database with data if it doesn't already exist.

    Args:
        session: The database session.
        data: A list of dictionaries containing the data to seed.
        model: The SQLAlchemy model to use.
        name_field: The name of the field to check for existence.
    """
    for item in data:
        instance = await session.execute(
            select(model).where(getattr(model, name_field) == item[name_field])
        )
        if not instance.scalars().first():
            session.add(model(**item))
    await session.commit()


async def main():
    """
    Main function to seed the database.
    """
    settings = Settings()
    session_maker = get_session_maker(settings)
    async with session_maker() as session:
        with open("pizza.json", "r") as f:
            pizzas_data = json.load(f)

        pizzas_to_seed = [
            {
                "name": p["name"],
                "base_price": p["price"],
                "image_url": p["img"],
                "ingredients": p["ingredients"],
            }
            for p in pizzas_data
        ]
        await seed_data(session, pizzas_to_seed, Pizza, "name")

        with open("extras.json", "r") as f:
            extras_data = json.load(f)
        await seed_data(session, extras_data, Extra, "name")

if __name__ == "__main__":
    asyncio.run(main())