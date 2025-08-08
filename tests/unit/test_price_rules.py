from decimal import Decimal

from app.db.models import Extra, Pizza
from app.core.price_rules import PriceCalculator


def test_calculate_unit_price():
    pizza = Pizza(base_price=Decimal("10.00"))
    extras = [Extra(price=Decimal("1.50")), Extra(price=Decimal("2.00"))]
    unit_price = PriceCalculator.calculate_unit_price(pizza, extras)
    assert unit_price == Decimal("13.50")


def test_calculate_line_total():
    pizza = Pizza(base_price=Decimal("10.00"))
    extras = [Extra(price=Decimal("1.50")), Extra(price=Decimal("2.00"))]
    line_total = PriceCalculator.calculate_line_total(pizza, extras, 2)
    assert line_total == Decimal("27.00")
