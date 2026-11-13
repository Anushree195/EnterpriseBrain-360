
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, ConfigDict, Field


# ==========================================
# CUSTOMER SCHEMAS
# ==========================================

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


# ==========================================
# SUPPORT TICKET SCHEMAS
# ==========================================

class TicketCreate(BaseModel):
    customer_id: int = Field(gt=0)
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)

    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed"
    ] = "open"

    priority: Literal[
        "low",
        "medium",
        "high",
        "urgent"
    ] = "medium"


class TicketUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None

    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed"
    ] | None = None

    priority: Literal[
        "low",
        "medium",
        "high",
        "urgent"
    ] | None = None


class TicketResponse(BaseModel):
    ticket_id: int
    customer_id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime


# ==========================================
# CUSTOMER INTERACTION SCHEMAS
# ==========================================

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


class InteractionResponse(BaseModel):
    interaction_id: int
    customer_id: int
    ticket_id: int | None
    interaction_type: str
    summary: str
    created_at: datetime


# ==========================================
# CUSTOMER 360 SCHEMA
# ==========================================

class Customer360Profile(BaseModel):
    customer_id: int
    name: str
    email: EmailStr
    company: str | None
    created_at: datetime

    tickets: list[TicketResponse]
    interactions: list[InteractionResponse]


# ==========================================
# AI COPILOT SCHEMAS
# ==========================================

class CopilotRequest(BaseModel):
    # Optional for general enterprise knowledge queries.
    # Required only when customer-specific context is selected.
    customer_id: int | None = Field(default=None, gt=0)

    question: str = Field(
        min_length=3,
        max_length=1000
    )


class CopilotResponse(BaseModel):
    # None for general enterprise knowledge queries.
    customer_id: int | None = None

    question: str
    answer: str
    knowledge_status: str
    sources: list[dict]
