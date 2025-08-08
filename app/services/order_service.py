import uuid
from decimal import Decimal

from app.core.errors import NotFoundAppError
from app.db.models import Order, OrderItem
from app.domain.price_rules import PriceCalculator
from app.repos.extra_repo import ExtraRepo
from app.repos.order_repo import OrderRepo
from app.repos.pizza_repo import PizzaRepo
from app.schemas.order import OrderIn


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepo,
        pizza_repo: PizzaRepo,
        extra_repo: ExtraRepo,
    ):
        self.order_repo = order_repo
        self.pizza_repo = pizza_repo
        self.extra_repo = extra_repo

    async def create_order(self, order_in: OrderIn) -> Order:
        order_items = []
        subtotal = Decimal(0)
        extras_total = Decimal(0)
        for line in order_in.lines:
            pizza = await self.pizza_repo.get(line.pizza_id)
            if not pizza:
                raise NotFoundAppError(f"Pizza with id {line.pizza_id} not found")

            extras = [await self.extra_repo.get(extra_id) for extra_id in line.extras]
            if any(e is None for e in extras):
                raise NotFoundAppError("One or more extras not found")
            unit_base_price = Decimal(pizza.base_price)
            unit_extras_total = sum(Decimal(extra.price) for extra in extras if extra)
            line_total = PriceCalculator.calculate_line_total(
                pizza, [e for e in extras if e], line.quantity
            )
            subtotal += line_total
            extras_total += unit_extras_total * line.quantity

            order_items.append(
                OrderItem(
                    pizza_id=line.pizza_id,
                    quantity=line.quantity,
                    selected_extras=[extra.id for extra in extras if extra],
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
        return await self.order_repo.create(order)

    async def get_order(self, order_id: uuid.UUID) -> Order:
        order = await self.order_repo.get(order_id)
        if not order:
            raise NotFoundAppError(f"Order with id {order_id} not found")
        return order
