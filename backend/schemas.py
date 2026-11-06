from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company: str | None = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    name: str
    email: EmailStr
    company: str | None
    created_at: datetime




from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime


# Data required to create a ticket
class TicketCreate(BaseModel):
    customer_id: int = Field(gt=0)
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    status: Literal["open", "in_progress", "resolved", "closed"] = "open"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"


# Data allowed when updating a ticket
class TicketUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None
    status: Literal["open", "in_progress", "resolved", "closed"] | None = None
    priority: Literal["low", "medium", "high", "urgent"] | None = None


# Data returned by the API
class TicketResponse(BaseModel):
    ticket_id: int
    customer_id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime





from typing import Literal


# Data required to create an interaction
class InteractionCreate(BaseModel):
    customer_id: int = Field(gt=0)
    ticket_id: int | None = Field(default=None, gt=0)

    interaction_type: Literal[
        "email",
        "phone",
        "chat",
        "meeting",
        "note"
    ]

    summary: str = Field(min_length=3)


# Data returned by the API
class InteractionResponse(BaseModel):
    interaction_id: int
    customer_id: int
    ticket_id: int | None
    interaction_type: str
    summary: str
    created_at: datetime


class Customer360Profile(BaseModel):
    customer_id: int
    name: str
    email: EmailStr
    company: str | None
    created_at: datetime

    tickets: list[TicketResponse]
    interactions: list[InteractionResponse]

class CopilotRequest(BaseModel):
    customer_id: int = Field(gt=0)
    question: str = Field(
        min_length=3,
        max_length=1000
    )


class CopilotResponse(BaseModel):
    customer_id: int
    question: str
    answer: str
    knowledge_status: str
    sources: list[dict]

