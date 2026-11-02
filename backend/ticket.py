
from fastapi import APIRouter, HTTPException, status
from psycopg.errors import ForeignKeyViolation

from database import get_connection
from schemas import TicketCreate, TicketUpdate, TicketResponse


router = APIRouter(prefix="/tickets", tags=["Support Tickets"])


# 1. Create a support ticket
@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(ticket: TicketCreate):

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO support_tickets
                    (customer_id, subject, description, status, priority)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING ticket_id, customer_id, subject,
                              description, status, priority, created_at;
                    """,
                    (
                        ticket.customer_id,
                        ticket.subject,
                        ticket.description,
                        ticket.status,
                        ticket.priority
                    )
                )

                return cursor.fetchone()

    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="Customer not found. Please provide a valid customer ID."
        )


# 2. Get all support tickets
@router.get("/", response_model=list[TicketResponse])
def get_tickets():

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT ticket_id, customer_id, subject,
                       description, status, priority, created_at
                FROM support_tickets
                ORDER BY ticket_id;
                """
            )

            return cursor.fetchall()


# 3. Get a ticket by ID
@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):

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

            return ticket


# 4. Update a support ticket
@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketUpdate):

    update_data = ticket.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update."
        )

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null."
        )

    allowed_fields = {"subject", "description", "status", "priority"}

    assignments = ", ".join(
        f"{field} = %s" for field in update_data
        if field in allowed_fields
    )

    values = list(update_data.values())

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                f"""
                UPDATE support_tickets
                SET {assignments}
                WHERE ticket_id = %s
                RETURNING ticket_id, customer_id, subject,
                          description, status, priority, created_at;
                """,
                (*values, ticket_id)
            )

            updated_ticket = cursor.fetchone()

            if updated_ticket is None:
                raise HTTPException(
                    status_code=404,
                    detail="Support ticket not found."
                )

            return updated_ticket


# 5. Delete a support ticket
@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM support_tickets
                WHERE ticket_id = %s
                RETURNING ticket_id;
                """,
                (ticket_id,)
            )

            deleted_ticket = cursor.fetchone()

            if deleted_ticket is None:
                raise HTTPException(
                    status_code=404,
                    detail="Support ticket not found."
                )

            return {
                "message": "Support ticket deleted successfully.",
                "ticket_id": deleted_ticket["ticket_id"]
            }
