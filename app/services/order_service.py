import uuid
from decimal import Decimal

from app.core.exceptions import NotFoundAppError
from app.db.models import Order, OrderItem, CustomerInfo
from app.core.price_rules import PriceCalculator
from app.db.repositories.cart_repo import CartRepo
from app.db.repositories.order_repo import OrderRepo
from app.db.repositories.customer_repo import CustomerInfoRepo
from app.db.repositories.pizza_repo import PizzaRepo
from app.db.repositories.extra_repo import ExtraRepo
from app.schemas.order import OrderIn, OrderLineIn, QuoteOrderLineOut, QuoteOut, OrderLineOut, OrderOut
from typing import List


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepo,
        cart_repo: CartRepo,
        customer_repo: CustomerInfoRepo,
        pizza_repo: PizzaRepo,
        extra_repo: ExtraRepo,
    ):
        self._order_repo = order_repo
        self._cart_repo = cart_repo
        self._customer_repo = customer_repo
        self._pizza_repo = pizza_repo
        self._extra_repo = extra_repo

    async def calculate_quote(self, lines: List[OrderLineIn]) -> QuoteOut:
        """Calculate price quote for order lines."""
        order_items = []
        subtotal = Decimal(0)
        extras_total = Decimal(0)

        for line in lines:
            # Validate pizza exists
            pizza = await self._pizza_repo.get(line.pizza_id)
            if not pizza:
                raise NotFoundAppError(f"Pizza with id {line.pizza_id} not found")

            # Validate extras exist
            extras = []
            for extra_id in line.extras:
                extra = await self._extra_repo.get(extra_id)
                if not extra:
                    raise NotFoundAppError(f"Extra with id {extra_id} not found")
                extras.append(extra)

            # Calculate prices
            unit_base_price = Decimal(str(pizza.base_price))
            unit_extras_total = sum(Decimal(str(extra.price)) for extra in extras)
            line_total = (unit_base_price + unit_extras_total) * line.quantity

            subtotal += unit_base_price * line.quantity
            extras_total += unit_extras_total * line.quantity

            order_items.append(
                QuoteOrderLineOut(
                
                    pizza_id=line.pizza_id,
                    quantity=line.quantity,
                    extras=line.extras,
                    unit_base_price=float(unit_base_price),
                    unit_extras_total=float(unit_extras_total),
                    line_total=float(line_total),
                )
            )

        grand_total = subtotal + extras_total

        return QuoteOut(
            subtotal=float(subtotal),
            extras_total=float(extras_total),
            grand_total=float(grand_total),
            lines=order_items,
        )

    async def create_order(self, order_in: OrderIn) -> OrderOut:
        # Find or create customer
        unique_identifier = order_in.customer.unique_identifier
        customer = await self._customer_repo.find_or_create(
            unique_identifier=unique_identifier,
            fullname=order_in.customer.fullname,
            full_address=order_in.customer.full_address,
        )

        # Calculate order details
        quote = await self.calculate_quote(order_in.lines)

        # Create order items
        order_items = []
        for line_data in quote.lines:
            order_items.append(
                OrderItem(
                    pizza_id=line_data.pizza_id,
                    quantity=line_data.quantity,
                    selected_extras=[str(e) for e in line_data.extras],
                    unit_base_price=Decimal(str(line_data.unit_base_price)),
                    unit_extras_total=Decimal(str(line_data.unit_extras_total)),
                    line_total=Decimal(str(line_data.line_total)),
                )
            )

        order = Order(
            uniqueIdentifier=unique_identifier,
            customer_id=customer.id,
            status="created",
            subtotal=Decimal(str(quote.subtotal)),
            extras_total=Decimal(str(quote.extras_total)),
            grand_total=Decimal(str(quote.grand_total)),
            items=order_items,
        )
        created_order = await self._order_repo.create(order)
        print(created_order)
        return OrderOut.model_validate(created_order)

    async def get_order(self, order_id: uuid.UUID) -> Order:
        order = await self._order_repo.get(order_id)
        if not order:
            raise NotFoundAppError(f"Order with id {order_id} not found")
        return order
