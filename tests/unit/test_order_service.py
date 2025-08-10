import pytest
import uuid
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from app.services.order_service import OrderService
from app.core.exceptions import NotFoundAppError
from app.schemas.order import OrderLineIn, OrderIn, QuoteOut
from app.schemas.customer import CustomerInfoIn
from tests.conftest import create_pizza, create_extra, create_customer, create_order


class TestOrderService:
    """Test cases for OrderService"""

    @pytest.fixture
    def order_service(self, mock_uow):
        """OrderService instance with mocked dependencies"""
        return OrderService(mock_uow)

    @pytest.mark.asyncio
    async def test_calculate_quote_success(self, order_service, mock_uow):
        """Test the complex price calculation logic"""
        # Arrange
        pizza1 = create_pizza(
            id=uuid.uuid4(),
            name="Margherita",
            base_price=Decimal("12.99")
        )
        pizza2 = create_pizza(
            id=uuid.uuid4(),
            name="Pepperoni",
            base_price=Decimal("15.99")
        )
        extra1 = create_extra(
            id=uuid.uuid4(),
            name="Extra Cheese",
            price=Decimal("2.50")
        )
        extra2 = create_extra(
            id=uuid.uuid4(),
            name="Mushrooms",
            price=Decimal("1.75")
        )

        order_lines = [
            OrderLineIn(
                pizza_id=pizza1.id,
                quantity=2,
                extras=[extra1.id]
            ),
            OrderLineIn(
                pizza_id=pizza2.id,
                quantity=1,
                extras=[extra1.id, extra2.id]
            )
        ]

        # Mock repository calls
        async def mock_pizza_get(pizza_id):
            if pizza_id == pizza1.id:
                return pizza1
            elif pizza_id == pizza2.id:
                return pizza2
            return None

        async def mock_extra_get(extra_id):
            if extra_id == extra1.id:
                return extra1
            elif extra_id == extra2.id:
                return extra2
            return None

        mock_uow.pizzas.get = AsyncMock(side_effect=mock_pizza_get)
        mock_uow.extras.get = AsyncMock(side_effect=mock_extra_get)

        # Act
        result = await order_service.calculate_quote(order_lines)

        # Assert
        assert isinstance(result, QuoteOut)
        assert len(result.lines) == 2

        # First line: 2 x (12.99 + 2.50) = 2 x 15.49 = 30.98
        line1 = result.lines[0]
        assert line1.pizza_id == pizza1.id
        assert line1.quantity == 2
        assert line1.unit_base_price == 12.99
        assert line1.unit_extras_total == 2.50
        assert line1.line_total == 30.98

        # Second line: 1 x (15.99 + 2.50 + 1.75) = 20.24
        line2 = result.lines[1]
        assert line2.pizza_id == pizza2.id
        assert line2.quantity == 1
        assert line2.unit_base_price == 15.99
        assert line2.unit_extras_total == 4.25
        assert line2.line_total == 20.24

        # Totals
        expected_subtotal = (12.99 * 2) + (15.99 * 1)  # 41.97
        expected_extras_total = (2.50 * 2) + (4.25 * 1)  # 9.25
        expected_grand_total = expected_subtotal + expected_extras_total  # 51.22

        assert result.subtotal == expected_subtotal
        assert result.extras_total == expected_extras_total
        assert result.grand_total == expected_grand_total

    @pytest.mark.asyncio
    async def test_create_order_success(self, order_service, mock_uow):
        """Test the full order creation workflow"""
        # Arrange
        pizza = create_pizza(
            id=uuid.uuid4(),
            name="Margherita",
            base_price=Decimal("12.99")
        )
        extra = create_extra(
            id=uuid.uuid4(),
            name="Extra Cheese",
            price=Decimal("2.50")
        )
        customer = create_customer(
            uniqueIdentifier="test_customer",
            fullname="John Doe",
            full_address="123 Test St"
        )

        order_in = OrderIn(
            lines=[
                OrderLineIn(
                    pizza_id=pizza.id,
                    quantity=1,
                    extras=[extra.id]
                )
            ],
            customer=CustomerInfoIn(
                unique_identifier="test_customer",
                fullname="John Doe",
                full_address="123 Test St"
            )
        )

        created_order = create_order(
            uniqueIdentifier="test_customer",
            customer_id=customer.id,
            status="created",
            subtotal=Decimal("12.99"),
            extras_total=Decimal("2.50"),
            grand_total=Decimal("15.49")
        )

        # Mock repository calls
        mock_uow.pizzas.get = AsyncMock(return_value=pizza)
        mock_uow.extras.get = AsyncMock(return_value=extra)
        mock_uow.customers.find_or_create = AsyncMock(return_value=customer)
        mock_uow.orders.create = AsyncMock(return_value=created_order)

        # Act
        result = await order_service.create_order(order_in)

        # Assert
        assert result.unique_identifier == "test_customer"
        assert result.status == "created"
        assert result.subtotal == 12.99
        assert result.extras_total == 2.50
        assert result.grand_total == 15.49

        # Verify repository calls
        mock_uow.customers.find_or_create.assert_called_once_with(
            unique_identifier="test_customer",
            fullname="John Doe",
            full_address="123 Test St"
        )
        mock_uow.orders.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_calculate_quote_invalid_extra(self, order_service, mock_uow):
        """Test validation when extra doesn't exist"""
        # Arrange
        pizza = create_pizza(
            id=uuid.uuid4(),
            name="Margherita",
            base_price=Decimal("12.99")
        )
        invalid_extra_id = uuid.uuid4()

        order_lines = [
            OrderLineIn(
                pizza_id=pizza.id,
                quantity=1,
                extras=[invalid_extra_id]
            )
        ]

        # Mock repository calls
        mock_uow.pizzas.get = AsyncMock(return_value=pizza)
        mock_uow.extras.get = AsyncMock(return_value=None)  # Extra not found

        # Act & Assert
        with pytest.raises(NotFoundAppError) as exc_info:
            await order_service.calculate_quote(order_lines)
        
        assert f"Extra with id {invalid_extra_id} not found" in str(exc_info.value)
        mock_uow.extras.get.assert_called_with(invalid_extra_id)