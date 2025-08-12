import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.limiter import limiter
from app.core.response import Response, ok, paginated
from app.db.session import get_session_maker
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.order_repo import OrderRepo
from app.schemas.order import OrderIn, OrderOut, QuoteOut, OrderLineIn
from app.services.order_service import OrderService
from app.core.config import get_settings
from app.api.deps import get_order_service

router = APIRouter()


@router.post(
    "/checkout",
    response_model=Response[OrderOut],
    summary="Checkout and create an order",
    description="""
This endpoint handles the final checkout process. It takes customer information and a list of order lines,
validates the data, calculates the final price, and creates an order in the system.
""",
)
@limiter.limit("5/minute")
async def checkout_order(
    request: Request,
    order_in: OrderIn,
    order_service: OrderService = Depends(get_order_service),
):
    """Create an order with customer details and order lines."""
    order = await order_service.create_order(order_in)
    return ok(order)


@router.post(
    "/quote",
    response_model=Response[QuoteOut],
    summary="Get a price quote for an order",
    description="""
Calculates the total price for a given list of order lines without creating an order.
This is useful for providing a price estimate to the customer before they proceed to checkout.
""",
)
async def quote_order(
    lines: list[OrderLineIn],
    order_service: OrderService = Depends(get_order_service),
):
    """Calculate price quote for a list of order lines."""
    quote = await order_service.calculate_quote(lines)
    return ok(quote)


@router.get(
    "/{order_id}",
    response_model=Response[OrderOut],
    summary="Get a specific order by its ID",
    description="Retrieves the details of a single order using its unique identifier.",
)
async def get_order(
    order_id: uuid.UUID,
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order(order_id)
    return ok(order)


@router.get(
    "/",
    response_model=Response[list[OrderOut]],
    summary="Get all orders",
    description="Retrieves a list of all orders.",
)
async def get_all_orders(
    unique_identifier: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    order_service: OrderService = Depends(get_order_service),
):
    skip = (page - 1) * per_page
    result = await order_service.get_all_orders(
        unique_identifier=unique_identifier, skip=skip, limit=per_page
    )
    return paginated(
        result["items"], page=page, size=per_page, total=result["total"]
    )
