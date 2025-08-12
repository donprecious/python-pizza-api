import uuid
from pydantic import BaseModel, Field, AliasChoices


class CustomerInfoIn(BaseModel):
    
    unique_identifier: str = Field(..., min_length=1,
                                   description="Unique identifier for the customer. eg email or randon string.")

    fullname: str = Field(..., min_length=1, description="Full name of the customer.")
    full_address: str = Field(
        ..., min_length=1, description="Full address of the customer."
    )


class CustomerInfoOut(BaseModel):
    id: uuid.UUID
    unique_identifier: str = Field(
        validation_alias=AliasChoices("uniqueIdentifier", "unique_identifier"),
    )
    fullname: str
    full_address: str = Field(
        validation_alias=AliasChoices("full_address", "full_address"),
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class CustomerInfoUpdate(BaseModel):
    fullname: str | None = None
    full_address: str | None = None