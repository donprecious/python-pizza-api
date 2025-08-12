from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings, get_settings


def get_session_maker() -> async_sessionmaker:
    engine = create_async_engine(get_settings().db_url)
    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session
