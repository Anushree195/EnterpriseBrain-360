
from datetime import datetime


def format_datetime(value: datetime | None) -> str:
    """Convert datetime values into readable strings."""

    if value is None:
        return "Not available"

    return value.strftime("%Y-%m-%d %H:%M:%S")


def format_customer_context(context: dict) -> str:
    """
    Convert customer profile, tickets and interactions
    into structured text for the AI Copilot.
    """

    if not context:
        raise ValueError("Customer context cannot be empty.")

    customer = context.get("customer")

    if not customer:
        raise ValueError("Customer profile is missing.")

    tickets = context.get("tickets", [])
    interactions = context.get("interactions", [])

    lines = []

    # 1. Customer profile
    lines.append("CUSTOMER PROFILE")
    lines.append(f"Customer ID: {customer['customer_id']}")
    lines.append(f"Name: {customer['name']}")
    lines.append(f"Email: {customer['email']}")
    lines.append(f"Company: {customer.get('company') or 'Not available'}")
    lines.append(
        f"Customer Since: {format_datetime(customer.get('created_at'))}"
    )

    # 2. Support tickets
    lines.append("\nSUPPORT TICKETS")

    if not tickets:
        lines.append("No support tickets found.")

    else:
        for ticket in tickets:
            lines.append(f"\nTicket ID: {ticket['ticket_id']}")
            lines.append(f"Subject: {ticket['subject']}")
            lines.append(f"Description: {ticket['description']}")
            lines.append(f"Status: {ticket['status']}")
            lines.append(f"Priority: {ticket['priority']}")
            lines.append(
                f"Created At: {format_datetime(ticket.get('created_at'))}"
            )

    # 3. Interaction history
    lines.append("\nINTERACTION HISTORY")

    if not interactions:
        lines.append("No previous interactions found.")

    else:
        for interaction in interactions:
            lines.append(
                f"\nInteraction ID: {interaction['interaction_id']}"
            )
            lines.append(f"Ticket ID: {interaction.get('ticket_id')}")
            lines.append(
                f"Type: {interaction['interaction_type']}"
            )
            lines.append(f"Summary: {interaction['summary']}")
            lines.append(
                f"Date: {format_datetime(interaction.get('created_at'))}"
            )

    return "\n".join(lines)
