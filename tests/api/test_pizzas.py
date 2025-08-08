import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_list_pizzas():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/")
    assert response.status_code == 200
    for pizza in response.json()["data"]:
        assert "ingredients" in pizza


@pytest.mark.asyncio
async def test_list_pizzas_with_search():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/?search=margherita")
    assert response.status_code == 200
    for pizza in response.json()["data"]:
        assert "margherita" in pizza["name"].lower()


@pytest.mark.asyncio
async def test_list_pizzas_with_ingredients():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/?ingredients=tomato")
    assert response.status_code == 200
    for pizza in response.json()["data"]:
        assert "tomato" in pizza["ingredients"]


@pytest.mark.asyncio
async def test_list_pizzas_with_min_price():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/?min_price=10")
    assert response.status_code == 200
    for pizza in response.json()["data"]:
        assert pizza["base_price"] >= 10


@pytest.mark.asyncio
async def test_list_pizzas_with_max_price():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/?max_price=10")
    assert response.status_code == 200
    for pizza in response.json()["data"]:
        assert pizza["base_price"] <= 10


@pytest.mark.asyncio
async def test_list_pizzas_with_pagination():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/?page=2&per_page=1")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["items"]) == 1
    assert data["meta"]["page"] == 2
    assert data["meta"]["per_page"] == 1
