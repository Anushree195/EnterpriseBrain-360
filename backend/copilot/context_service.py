
from database import get_connection


def get_customer_context(customer_id: int) -> dict | None:
    """
    Retrieve a complete customer context, including
    customer profile, support tickets and interactions.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Step 1: Retrieve customer profile
            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    email,
                    company,
                    created_at
                FROM customers
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            # Return None if customer does not exist
            if customer is None:
                return None

            # Step 2: Retrieve customer support tickets
            cursor.execute(
                """
                SELECT
                    ticket_id,
                    subject,
                    description,
                    status,
                    priority,
                    created_at
                FROM support_tickets
                WHERE customer_id = %s
                ORDER BY created_at DESC
                """,
                (customer_id,)
            )

            tickets = cursor.fetchall()

            # Step 3: Retrieve customer interactions
            cursor.execute(
                """
                SELECT
                    interaction_id,
                    ticket_id,
                    interaction_type,
                    summary,
                    created_at
                FROM interactions
                WHERE customer_id = %s
                ORDER BY created_at DESC
                """,
                (customer_id,)
            )

            interactions = cursor.fetchall()

            # Step 4: Assemble complete customer context
            customer_context = {
                "customer": customer,
                "tickets": tickets,
                "interactions": interactions
            }

            return customer_context

    finally:
        connection.close()
