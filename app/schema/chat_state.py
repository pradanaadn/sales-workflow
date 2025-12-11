from pydantic import BaseModel, Field

from app.schema.customer import CustomerSchema

class ChatState(BaseModel):
    telephone_number: str = Field(..., description="Customer's telephone number")
    customer_info: CustomerSchema | None = Field(default_factory=CustomerSchema, description="Customer information")
    user_chat: str = Field(..., description="User's chat message")
    agent_response: str | dict | None = Field(None, description="Agent's response message")
    number_of_parse: int = Field(0, description="Number of times customer info has been parsed")
    def is_known_customer(self) -> bool:
        return self.customer_info.name is not None and self.customer_info.location is not None