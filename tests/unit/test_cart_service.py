import pytest
import uuid
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from app.services.cart_service import CartService
from app.core.exceptions import NotFoundAppError
from app.schemas.cart import CartItemIn
from app.schemas.customer import CustomerInfoIn
from tests.conftest import create_pizza, create_extra, create_cart, create_cart_item


class TestCartService:
    """Test cases for CartService"""

    @pytest.fixture
    def order_service_mock(self):
        """Mock OrderService for CartService dependency"""
        return Mock()

    @pytest.fixture
    def cart_service(self, mock_uow, order_service_mock):
        """CartService instance with mocked dependencies"""
        return CartService(mock_uow, order_service_mock)

    @pytest.mark.asyncio
    async def test_calculate_cart_totals_with_extras(self, cart_service, mock_uow):
        """Test the core price calculation logic in _calculate_cart_totals()"""
        # Arrange
        pizza = create_pizza(
            id=uuid.uuid4(),
            name="Margherita",
            base_price=Decimal("12.99")
        )
        extra1 = create_extra(
            id=uuid.uuid4(),
            name="Extra Cheese",
            price=Decimal("2.50")
        )
        extra2 = create_extra(
            id=uuid.uuid4(),
            name="Pepperoni",
            price=Decimal("3.00")
        )
        
        cart = create_cart(uniqueIdentifier="test_cart")
        cart_item = create_cart_item(
            cart_id=cart.id,
            pizza_id=pizza.id,
            quantity=2,
            selected_extras=[str(extra1.id), str(extra2.id)]
        )
        cart.items = [cart_item]

        # Mock repository calls
        mock_uow.pizzas.get = AsyncMock(return_value=pizza)
        mock_uow.extras.get_many = AsyncMock(return_value=[extra1, extra2])

        # Act
        result = await cart_service._calculate_cart_totals(cart)

        # Assert
        expected_unit_price = Decimal("12.99") + Decimal("2.50") + Decimal("3.00")  # 18.49
        expected_total_price = expected_unit_price * 2  # 36.98
        
        assert len(result.items) == 1
        assert result.items[0].unit_price == float(expected_unit_price)
        assert result.items[0].total_price == float(expected_total_price)
        assert result.subtotal == float(expected_total_price)
        assert result.grand_total == float(expected_total_price)
        
        # Verify repository calls
        mock_uow.pizzas.get.assert_called_once_with(pizza.id)
        mock_uow.extras.get_many.assert_called_once_with([extra1.id, extra2.id])

    @pytest.mark.asyncio
    async def test_add_to_cart_pizza_not_found(self, cart_service, mock_uow):
        """Test error handling when pizza doesn't exist"""
        # Arrange
        cart = create_cart(uniqueIdentifier="test_cart")
        pizza_id = uuid.uuid4()
        
        cart_item_in = CartItemIn(
            unique_identifier="test_cart",
            pizza_id=pizza_id,
            quantity=1,
            extras=[]
        )

        # Mock repository calls
        mock_uow.carts.find_or_create = AsyncMock(return_value=cart)
        mock_uow.pizzas.get = AsyncMock(return_value=None)  # Pizza not found

        # Act & Assert
        with pytest.raises(NotFoundAppError) as exc_info:
            await cart_service.add_to_cart(cart_item_in, "test_cart")
        
        assert f"Pizza with id {pizza_id} not found" in str(exc_info.value)
        mock_uow.pizzas.get.assert_called_once_with(pizza_id)

    @pytest.mark.asyncio
    async def test_checkout_empty_cart(self, cart_service, mock_uow, order_service_mock):
        """Test validation for empty cart checkout"""
        # Arrange
        customer_info = CustomerInfoIn(
            unique_identifier="test_customer",
            fullname="John Doe",
            full_address="123 Test St"
        )
        
        # Mock empty cart
        empty_cart = create_cart(uniqueIdentifier="test_customer")
        empty_cart.items = []
        
        mock_uow.carts.find_or_create = AsyncMock(return_value=empty_cart)

        # Act & Assert
        with pytest.raises(NotFoundAppError) as exc_info:
            await cart_service.checkout(customer_info)
        
        assert "Cannot checkout with an empty cart" in str(exc_info.value)