from pydantic import BaseModel, Field

from app.schema.customer import CustomerSchema

class ChatState(BaseModel):
    telephone_number: str = Field(..., description="Customer's telephone number")
    customer_info: CustomerSchema | None = Field(default_factory=CustomerSchema, description="Customer information")
    user_chat: str = Field(..., description="User's chat message")
    agent_response: str | dict | None = Field(None, description="Agent's response message")
    
    def is_known_customer(self) -> bool:
        return self.customer_info.name is not None