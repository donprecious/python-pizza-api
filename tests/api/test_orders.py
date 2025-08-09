import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_order_quote():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add an item to the cart first
        await ac.post(
            "/api/carts/items",
            json={"pizza_id": 1, "quantity": 2},
            headers={"x-unique-identifier": "quote-user"},
        )

        # Now, create an order quote
        response = await ac.post(
            "/api/orders/quote",
            headers={"x-unique-identifier": "quote-user"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total_price"] > 0
    assert data["data"]["customer"]["unique_identifier"] == "quote-user"


@pytest.mark.asyncio
async def test_checkout_order():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add an item to the cart
        await ac.post(
            "/api/carts/items",
            json={"pizza_id": 2, "quantity": 1},
            headers={"x-unique-identifier": "checkout-user"},
        )

        # Create a quote
        quote_response = await ac.post(
            "/api/orders/quote",
            headers={"x-unique-identifier": "checkout-user"},
        )
        quote_data = quote_response.json()
        order_id = quote_data["data"]["id"]

        # Checkout
        response = await ac.post(
            f"/api/orders/checkout",
            json={
                "order_id": order_id,
                "customer_details": {
                    "name": "John Doe",
                    "address": "123 Main St",
                    "phone": "555-555-5555",
                },
            },
            headers={"x-unique-identifier": "checkout-user"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "pending"
    assert data["data"]["customer"]["name"] == "John Doe"


@pytest.mark.asyncio
async def test_get_order_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create an order first
        await ac.post(
            "/api/carts/items",
            json={"pizza_id": 1, "quantity": 1},
            headers={"x-unique-identifier": "get-order-user"},
        )
        quote_response = await ac.post(
            "/api/orders/quote",
            headers={"x-unique-identifier": "get-order-user"},
        )
        order_id = quote_response.json()["data"]["id"]

        # Get the order
        response = await ac.get(
            f"/api/orders/{order_id}",
            headers={"x-unique-identifier": "get-order-user"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == order_id


@pytest.mark.asyncio
async def test_list_orders():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create an order
        await ac.post(
            "/api/carts/items",
            json={"pizza_id": 3, "quantity": 1},
            headers={"x-unique-identifier": "list-orders-user"},
        )
        await ac.post(
            "/api/orders/quote",
            headers={"x-unique-identifier": "list-orders-user"},
        )

        # List orders
        response = await ac.get(
            "/api/orders/", headers={"x-unique-identifier": "list-orders-user"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) > 0