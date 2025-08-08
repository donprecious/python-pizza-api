import uuid
from typing import List

from pydantic import BaseModel, Field


class CartItemIn(BaseModel):
    pizza_id: uuid.UUID
    quantity: int = Field(gt=0, le=99)
    extras: List[uuid.UUID] = []


class CartItemOut(BaseModel):
    id: uuid.UUID
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID]
    unit_price: float
    total_price: float

    class Config:
        orm_mode = True


class CartOut(BaseModel):
    id: uuid.UUID
    items: List[CartItemOut]
    subtotal: float
    grand_total: float

    class Config:
        orm_mode = True
