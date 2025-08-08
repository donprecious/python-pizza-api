import asyncio
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routers import carts, extras, health, orders, pizzas
from app.core.exception_handler import add_exception_handlers
from app.core.limiter import limiter
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Usersnack API",
        description="A FastAPI backend for a pizza ordering service.",
        version="0.1.0",
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    app.include_router(pizzas.router, prefix="/api/pizzas", tags=["pizzas"])
    app.include_router(extras.router, prefix="/api/extras", tags=["extras"])
    app.include_router(carts.router, prefix="/api/carts", tags=["carts"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(health.router, prefix="/health", tags=["health"])

    add_exception_handlers(app)

    return app


app = create_app()
