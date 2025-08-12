import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routers import carts, extras, health, orders, pizzas
from app.core.exception_handler import add_exception_handlers
from app.core.limiter import limiter
from app.core.logging import setup_logging
from scripts.seed import seed_db
import logging

from app.core.config import get_settings
from app.db.session import get_session_maker
from app.db.uow import UnitOfWork

log = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    log.info("seed database...")
    session_maker = get_session_maker()

    async with session_maker() as session:
        uow = UnitOfWork(session)
        async with uow:
            await seed_db(uow)
    yield

def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()

    app = FastAPI(
        title="Usersnack API",
        description="A FastAPI backend for a pizza ordering service.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
