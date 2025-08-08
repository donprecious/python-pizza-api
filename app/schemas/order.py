import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class OrderLineIn(BaseModel):
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID] = []


class OrderIn(BaseModel):
    email: EmailStr
    lines: List[OrderLineIn]
    customer: Optional[dict] = None


class OrderLineOut(BaseModel):
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID]
    unit_base_price: float
    unit_extras_total: float
    line_total: float


class OrderOut(BaseModel):
    id: uuid.UUID
    status: str
    subtotal: float
    extras_total: float
    grand_total: float
    lines: List[OrderLineOut]

    class Config:
        orm_mode = True


class QuoteOut(BaseModel):
    subtotal: float
    extras_total: float
    grand_total: float
    lines: List[OrderLineOut]
