from decimal import Decimal, ROUND_HALF_EVEN
from typing import List

from app.db.models import Extra, Pizza


class PriceCalculator:
    @staticmethod
    def calculate_unit_price(pizza: Pizza, extras: List[Extra]) -> Decimal:
        unit_base = Decimal(pizza.base_price)
        unit_extras = sum(Decimal(extra.price) for extra in extras)
        return (unit_base + unit_extras).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

    @staticmethod
    def calculate_line_total(
        pizza: Pizza, extras: List[Extra], quantity: int
    ) -> Decimal:
        unit_total = PriceCalculator.calculate_unit_price(pizza, extras)
        return (unit_total * quantity).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
