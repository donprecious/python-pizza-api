import uuid

from pydantic import BaseModel


class Pizza(BaseModel):
    id: uuid.UUID
    name: str
    base_price: float
    image_url: str | None
    is_active: bool
    ingredients: list[str]

    class Config:
        from_attributes = True


class PizzaCreate(BaseModel):
    name: str
    base_price: float
    image_url: str | None
    is_active: bool
    ingredients: list[str]


class PizzaOut(BaseModel):
    id: uuid.UUID
    name: str
    base_price: float
    image_url: str | None
    is_active: bool
    ingredients: list[str]

    class Config:
        from_attributes = True


class ExtraOut(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    is_active: bool

    class Config:
        from_attributes = True


class PaginatedPizzaOut(BaseModel):
    items: list[PizzaOut]
    page: int
    page_size: int
    total: int


