import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, expected_status, expected_pizza_name, expected_ingredient, min_price, max_price, page, per_page",
    [
        ({}, 200, None, None, None, None, 1, 10),
        ({"search": "margherita"}, 200, "margherita", None, None, None, 1, 10),
        (
            {"ingredients": "tomato"},
            200,
            None,
            "tomato",
            None,
            None,
            1,
            10,
        ),
        ({"min_price": 10}, 200, None, None, 10, None, 1, 10),
        ({"max_price": 10}, 200, None, None, None, 10, 1, 10),
        ({"page": 2, "per_page": 1}, 200, None, None, None, None, 2, 1),
    ],
)
async def test_list_pizzas(
    params,
    expected_status,
    expected_pizza_name,
    expected_ingredient,
    min_price,
    max_price,
    page,
    per_page,
):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/pizzas/", params=params)

    assert response.status_code == expected_status
    response_data = response.json()

    if "items" in response_data["data"]:
        for pizza in response_data["data"]["items"]:
            assert "ingredients" in pizza
            if expected_pizza_name:
                assert expected_pizza_name in pizza["name"].lower()
            if expected_ingredient:
                assert expected_ingredient in pizza["ingredients"]
            if min_price:
                assert pizza["base_price"] >= min_price
            if max_price:
                assert pizza["base_price"] <= max_price

    if "meta" in response_data["data"]:
        meta = response_data["data"]["meta"]
        assert meta["page"] == page
        assert meta["per_page"] == per_page
