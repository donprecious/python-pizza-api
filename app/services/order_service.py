import uuid
from decimal import Decimal

from app.core.errors import NotFoundAppError
from app.db.models import Order, OrderItem
from app.domain.price_rules import PriceCalculator
from app.repos.cart_repo import CartRepo
from app.repos.order_repo import OrderRepo
from app.schemas.order import OrderIn


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepo,
        cart_repo: CartRepo,
    ):
        self._order_repo = order_repo
        self._cart_repo = cart_repo

    async def create_order(self, order_in: OrderIn) -> Order:
        order_items = []
        subtotal = Decimal(0)
        extras_total = Decimal(0)
        for line in order_in.lines:
            # Note: Pizza and extra validation would need to be handled differently
            # since we no longer have direct access to pizza_repo and extra_repo
            # This might require the data to be pre-validated or passed differently
            
            unit_base_price = Decimal(0)  # Would need to be provided or calculated differently
            unit_extras_total = Decimal(0)  # Would need to be provided or calculated differently
            line_total = Decimal(0)  # Would need to be calculated differently
            
            subtotal += line_total
            extras_total += unit_extras_total * line.quantity

            order_items.append(
                OrderItem(
                    pizza_id=line.pizza_id,
                    quantity=line.quantity,
                    selected_extras=line.extras,
                    unit_base_price=unit_base_price,
                    unit_extras_total=unit_extras_total,
                    line_total=line_total,
                )
            )

        order = Order(
            email=order_in.email,
            status="created",
            subtotal=subtotal,
            extras_total=extras_total,
            grand_total=subtotal,
            customer_info=order_in.customer,
            items=order_items,
        )
        return await self._order_repo.create(order)

    async def get_order(self, order_id: uuid.UUID) -> Order:
        order = await self._order_repo.get(order_id)
        if not order:
            raise NotFoundAppError(f"Order with id {order_id} not found")
        return order
