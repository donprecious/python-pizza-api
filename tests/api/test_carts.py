import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_add_item_to_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/carts/items",
            json={"pizza_id": 1, "quantity": 1},
            headers={"x-unique-identifier": "test-user"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["customer"]["unique_identifier"] == "test-user"
    assert len(data["data"]["items"]) == 1
    assert data["data"]["items"]["pizza"]["name"] == "Margherita"
    assert data["data"]["items"]["quantity"] == 1


@pytest.mark.asyncio
async def test_get_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, add an item to the cart
        await ac.post(
            "/api/carts/items",
            json={"pizza_id": 1, "quantity": 1},
            headers={"x-unique-identifier": "test-user-2"},
        )

        # Then, get the cart
        response = await ac.get(
            "/api/carts/", headers={"x-unique-identifier": "test-user-2"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["customer"]["unique_identifier"] == "test-user-2"
    assert len(data["data"]["items"]) == 1
    assert data["data"]["items"]["pizza"]["name"] == "Margherita"
    assert data["data"]["items"]["quantity"] == 1