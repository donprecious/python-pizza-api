import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, AliasChoices

from app.schemas.customer import CustomerInfoIn


class OrderLineIn(BaseModel):
    pizza_id: uuid.UUID
    quantity: int = Field(gt=0, description="Quantity of the pizza, must be greater than 0.")
    extras: List[uuid.UUID] = []

    @field_validator("pizza_id", mode="before")
    @classmethod
    def valid_uuid(cls, v):
        try:
            return uuid.UUID(str(v))
        except ValueError:
            raise ValueError("Invalid UUID format")


class OrderIn(BaseModel):
    lines: List[OrderLineIn]
    customer: CustomerInfoIn


class OrderLineOut(BaseModel):
    id: uuid.UUID
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID] =  Field(
        validation_alias=AliasChoices("extras", "selected_extras"),
    )
    unit_base_price: float
    unit_extras_total: float
    line_total: float

    class Config:
        from_attributes = True
        populate_by_name = True
    
class QuoteOrderLineOut(BaseModel):
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID] =  Field(
        validation_alias=AliasChoices("extras", "selected_extras"),
    )
    unit_base_price: float
    unit_extras_total: float
    line_total: float

    class Config:
        from_attributes = True
        populate_by_name = True

class OrderOut(BaseModel):
    id: uuid.UUID
    unique_identifier: str = Field(
        validation_alias=AliasChoices("uniqueIdentifier", "unique_identifier"),
    )
    status: str
    subtotal: float
    extras_total: float
    grand_total: float
    lines: List[OrderLineOut] = Field(validation_alias="items")

    class Config:
        from_attributes = True
        populate_by_name = True


class QuoteOut(BaseModel):
    subtotal: float
    extras_total: float
    grand_total: float
    lines: List[QuoteOrderLineOut]

    class Config:
        from_attributes = True
