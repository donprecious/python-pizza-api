import uuid
from typing import List

from pydantic import BaseModel, Field, field_validator, AliasChoices
from app.schemas.customer import CustomerInfoIn


class CartItemIn(BaseModel):
    unique_identifier: str = Field(..., min_length=1, description="Unique identifier for the cart, typically a email or any unique id.")
    pizza_id: uuid.UUID = Field(..., description="ID of the pizza to add to the cart.")
    quantity: int = Field(gt=0, le=99)
    extras: List[uuid.UUID] = Field([], description="List of extra IDs to add to the pizza.")

    @field_validator("pizza_id", "extras", mode="before")
    @classmethod
    def valid_uuid(cls, v):
        if isinstance(v, list):
            try:
                return [uuid.UUID(str(item)) for item in v]
            except ValueError:
                raise ValueError("Invalid UUID format in list")
        try:
            return uuid.UUID(str(v))
        except ValueError:
            raise ValueError("Invalid UUID format")


class CartItemOut(BaseModel):
    id: uuid.UUID
    pizza_id: uuid.UUID
    quantity: int
    extras: List[uuid.UUID]
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: uuid.UUID
    unique_identifier: str = Field(
        validation_alias=AliasChoices("uniqueIdentifier", "unique_identifier"),
    )
    items: List[CartItemOut]
    subtotal: float
    grand_total: float

    class Config:
        from_attributes = True
        populate_by_name = True


class CartCheckout(BaseModel):
    customer: CustomerInfoIn
