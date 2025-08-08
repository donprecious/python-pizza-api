import asyncio
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1 import carts, extras, health, orders, pizzas
from app.containers import Container
from app.core.exception_handler import add_exception_handlers
from app.core.limiter import limiter
from app.core.logging import setup_logging
from scripts.seed import main as seed_main


def create_app() -> FastAPI:
    setup_logging()

    container = Container()

    app = FastAPI(
        title="Usersnack API",
        description="A FastAPI backend for a pizza ordering service.",
        version="0.1.0",
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    app.container = container
    app.container.wire(
        modules=[
            "app.api.v1.extras",
            "app.api.v1.pizzas",
            "app.api.v1.carts",
            "app.api.v1.orders",
        ]
    )

    app.include_router(pizzas.router, prefix="/api/v1/pizzas", tags=["pizzas"])
    app.include_router(extras.router, prefix="/api/v1/extras", tags=["extras"])
    app.include_router(carts.router, prefix="/api/v1/carts", tags=["carts"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
    app.include_router(health.router, prefix="/health", tags=["health"])

    add_exception_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        await seed_main()

    return app


app = create_app()
