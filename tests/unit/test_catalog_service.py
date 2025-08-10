import pytest
import uuid
from decimal import Decimal
from unittest.mock import Mock, AsyncMock
from app.services.catalog_service import CatalogService
from app.core.exceptions import NotFoundAppError
from app.schemas.catalog import PizzaOut
from app.schemas.pagination import Page, PageMeta
from tests.conftest import create_pizza, create_extra


class TestCatalogService:
    """Test cases for CatalogService"""

    @pytest.fixture
    def catalog_service(self, mock_uow):
        """CatalogService instance with mocked dependencies"""
        return CatalogService(mock_uow)

    @pytest.mark.asyncio
    async def test_list_pizzas_with_filters(self, catalog_service, mock_uow):
        """Test pagination and filtering logic in list_pizzas()"""
        # Arrange
        pizza1 = create_pizza(
            name="Margherita",
            base_price=Decimal("12.99"),
            ingredients=["tomato", "mozzarella", "basil"]
        )
        pizza2 = create_pizza(
            name="Pepperoni",
            base_price=Decimal("15.99"),
            ingredients=["tomato", "mozzarella", "pepperoni"]
        )
        pizzas = [pizza1, pizza2]
        total_count = 2

        # Mock repository calls
        mock_uow.pizzas.get_all = AsyncMock(return_value=(pizzas, total_count))

        # Act
        result = await catalog_service.list_pizzas(
            search="pizza",
            ingredients=["tomato"],
            min_price=10.0,
            max_price=20.0,
            page=1,
            page_size=10
        )

        # Assert
        assert isinstance(result, Page)
        assert len(result.items) == 2
        assert all(isinstance(item, PizzaOut) for item in result.items)
        assert result.meta.total == 2
        assert result.meta.page == 1
        assert result.meta.per_page == 10

        # Verify repository was called with correct parameters
        mock_uow.pizzas.get_all.assert_called_once_with(
            search="pizza",
            ingredients=["tomato"],
            min_price=10.0,
            max_price=20.0,
            page=1,
            page_size=10
        )

    @pytest.mark.asyncio
    async def test_get_pizza_not_found(self, catalog_service, mock_uow):
        """Test error handling when pizza doesn't exist"""
        # Arrange
        pizza_id = uuid.uuid4()
        mock_uow.pizzas.get = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(NotFoundAppError) as exc_info:
            await catalog_service.get_pizza(pizza_id)
        
        assert f"Pizza with id {pizza_id} not found" in str(exc_info.value)
        mock_uow.pizzas.get.assert_called_once_with(pizza_id)