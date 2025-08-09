import asyncio
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from app.db.models import Extra, Pizza
from app.db.session import get_session_maker


from app.db.uow import UnitOfWork


async def seed_data(uow: UnitOfWork, data: list, model, name_field: str):
    """
    Seeds the database with data if it doesn't already exist.

    Args:
        uow: The UnitOfWork instance.
        data: A list of dictionaries containing the data to seed.
        model: The SQLAlchemy model to use.
        name_field: The name of the field to check for existence.
    """
    for item in data:
        instance = await uow._session.execute(
            select(model).where(getattr(model, name_field) == item[name_field])
        )
        if not instance.scalars().first():
            uow._session.add(model(**item))


async def seed_db(uow: UnitOfWork):
    """
    Main function to seed the database.
    """
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
    await seed_data(uow, pizzas_to_seed, Pizza, "name")

    with open("extras.json", "r") as f:
        extras_data = json.load(f)
    await seed_data(uow, extras_data, Extra, "name")

async def main():
    """
    Main function to seed the database.
    """
    await seed_db()

if __name__ == "__main__":
    asyncio.run(main())