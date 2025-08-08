from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import Settings


def get_session_maker(config: Settings) -> async_sessionmaker:
    engine = create_async_engine(config.db_url)
    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
