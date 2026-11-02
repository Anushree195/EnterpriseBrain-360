
from fastapi import APIRouter, HTTPException, status
from psycopg.errors import ForeignKeyViolation

from database import get_connection
from schemas import InteractionCreate, InteractionResponse


router = APIRouter(
    prefix="/interactions",
    tags=["Customer Interactions"]
)


# 1. Create a customer interaction
@router.post(
    "/",
    response_model=InteractionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_interaction(interaction: InteractionCreate):

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO interactions
                    (customer_id, ticket_id, interaction_type, summary)
                    VALUES (%s, %s, %s, %s)
                    RETURNING interaction_id, customer_id, ticket_id,
                              interaction_type, summary, created_at;
                    """,
                    (
                        interaction.customer_id,
                        interaction.ticket_id,
                        interaction.interaction_type,
                        interaction.summary
                    )
                )

                return cursor.fetchone()

    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="Customer or support ticket not found."
        )


# 2. Get all customer interactions
@router.get("/", response_model=list[InteractionResponse])
def get_interactions():

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT interaction_id, customer_id, ticket_id,
                       interaction_type, summary, created_at
                FROM interactions
                ORDER BY created_at DESC;
                """
            )

            return cursor.fetchall()


# 3. Get interactions for a particular customer
@router.get(
    "/customer/{customer_id}",
    response_model=list[InteractionResponse]
)
def get_customer_interactions(customer_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT interaction_id, customer_id, ticket_id,
                       interaction_type, summary, created_at
                FROM interactions
                WHERE customer_id = %s
                ORDER BY created_at DESC;
                """,
                (customer_id,)
            )

            return cursor.fetchall()


# 4. Get an interaction by ID
@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT interaction_id, customer_id, ticket_id,
                       interaction_type, summary, created_at
                FROM interactions
                WHERE interaction_id = %s;
                """,
                (interaction_id,)
            )

            interaction = cursor.fetchone()

            if interaction is None:
                raise HTTPException(
                    status_code=404,
                    detail="Interaction not found."
                )

            return interaction


# 5. Delete an interaction
@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM interactions
                WHERE interaction_id = %s
                RETURNING interaction_id;
                """,
                (interaction_id,)
            )

            deleted_interaction = cursor.fetchone()

            if deleted_interaction is None:
                raise HTTPException(
                    status_code=404,
                    detail="Interaction not found."
                )

            return {
                "message": "Interaction deleted successfully.",
                "interaction_id": deleted_interaction["interaction_id"]
            }
