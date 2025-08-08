import uuid

from pydantic import BaseModel


class PizzaOut(BaseModel):
    id: uuid.UUID
    name: str
    base_price: float
    image_url: str | None
    is_active: bool

    class Config:
        orm_mode = True


class ExtraOut(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    is_active: bool

    class Config:
        orm_mode = True
