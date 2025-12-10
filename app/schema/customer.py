from pydantic import BaseModel, Field


class CustomerSchema(BaseModel):
    name: str | None = Field(default=None, description="Customer's full name")
    location: str | None = Field(default=None, description="Customer's location address")