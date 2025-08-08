import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_list_pizzas():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/")
    assert response.status_code == 200
