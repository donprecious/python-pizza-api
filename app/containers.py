from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import get_settings, Settings
from app.db.session import get_session_maker
from app.repos.extra_repo import ExtraRepo
from app.repos.pizza_repo import PizzaRepo
from app.services.catalog_service import CatalogService


class Container(containers.DeclarativeContainer):
    config: providers.Provider[Settings] = providers.Singleton(get_settings)

    session_maker: providers.Provider[async_sessionmaker] = providers.Singleton(
        get_session_maker, config
    )

    pizza_repo: providers.Provider[PizzaRepo] = providers.Factory(
        PizzaRepo, session_maker
    )
    extra_repo: providers.Provider[ExtraRepo] = providers.Factory(
        ExtraRepo, session_maker
    )

    catalog_service: providers.Provider[CatalogService] = providers.Factory(
        CatalogService,
        pizza_repo=pizza_repo,
        extra_repo=extra_repo,
    )