
from fastapi import APIRouter, HTTPException

from database import get_connection

from workflows.ticket_classifier import classify_ticket
from workflows.priority_engine import recommend_priority
from workflows.resolution_engine import (
    generate_resolution_recommendation
)


router = APIRouter(
    prefix="/workflows",
    tags=["Intelligent Support Workflows"]
)


@router.get("/tickets/{ticket_id}/analyze")
def analyze_ticket(ticket_id: int):

    if ticket_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Ticket ID must be greater than zero."
        )

    # Step 1: Retrieve the ticket from PostgreSQL.
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT ticket_id, customer_id, subject,
                       description, status, priority, created_at
                FROM support_tickets
                WHERE ticket_id = %s;
                """,
                (ticket_id,)
            )

            ticket = cursor.fetchone()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Support ticket not found."
        )

    # Step 2: Classify the ticket.
    classification = classify_ticket(
        subject=ticket["subject"],
        description=ticket["description"]
    )

    # Step 3: Recommend priority.
    priority = recommend_priority(
        subject=ticket["subject"],
        description=ticket["description"]
    )

    # Step 4: Generate resolution recommendation.
    try:
        resolution = generate_resolution_recommendation(
            subject=ticket["subject"],
            description=ticket["description"]
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    # Step 5: Return combined workflow analysis.
    return {
        "ticket": {
            "ticket_id": ticket["ticket_id"],
            "customer_id": ticket["customer_id"],
            "subject": ticket["subject"],
            "description": ticket["description"],
            "current_status": ticket["status"],
            "current_priority": ticket["priority"],
            "created_at": ticket["created_at"]
        },
        "classification": classification,
        "priority_recommendation": priority,
        "resolution_recommendation": resolution
    }
