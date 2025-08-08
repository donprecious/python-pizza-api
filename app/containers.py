from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import get_session_maker
from app.repos.cart_repo import CartRepo
from app.repos.extra_repo import ExtraRepo
from app.repos.order_repo import OrderRepo
from app.repos.pizza_repo import PizzaRepo
from app.services.cart_service import CartService
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.pizzas",
            "app.api.v1.extras",
            "app.api.v1.carts",
            "app.api.v1.orders",
        ]
    )

    config = providers.Singleton(Settings)

    db = providers.Singleton(get_session_maker, config=config)

    pizza_repo = providers.Factory(PizzaRepo, session=db)
    extra_repo = providers.Factory(ExtraRepo, session=db)
    cart_repo = providers.Factory(CartRepo, session=db)
    order_repo = providers.Factory(OrderRepo, session=db)

    catalog_service = providers.Factory(
        CatalogService, pizza_repo=pizza_repo, extra_repo=extra_repo
    )
    cart_service = providers.Factory(
        CartService,
        cart_repo=cart_repo,
        pizza_repo=pizza_repo,
        extra_repo=extra_repo,
    )
    order_service = providers.Factory(
        OrderService,
        order_repo=order_repo,
        pizza_repo=pizza_repo,
        extra_repo=extra_repo,
    )
