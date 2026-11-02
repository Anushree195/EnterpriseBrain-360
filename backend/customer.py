
from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from database import get_connection

from schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    Customer360Profile
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# 1. Create customer
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(customer: CustomerCreate):

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO customers (name, email, company)
                    VALUES (%s, %s, %s)
                    RETURNING customer_id, name, email,
                              company, created_at;
                    """,
                    (
                        customer.name,
                        str(customer.email),
                        customer.company
                    )
                )

                return cursor.fetchone()

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email already exists."
        )


# 2. Get all customers
@router.get("/", response_model=list[CustomerResponse])
def get_customers():

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT customer_id, name, email, company, created_at
                FROM customers
                ORDER BY customer_id;
                """
            )

            return cursor.fetchall()


# 3. Get customer by ID
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT customer_id, name, email, company, created_at
                FROM customers
                WHERE customer_id = %s;
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            if customer is None:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found."
                )

            return customer


# 4. Update customer
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate):

    update_data = customer.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update."
        )

    allowed_fields = {"name", "email", "company"}

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null. Omit fields you do not want to update."
        )

    assignments = ", ".join(
        f"{field} = %s"
        for field in update_data
        if field in allowed_fields
    )

    values = [
        str(value) if field == "email" else value
        for field, value in update_data.items()
    ]

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    f"""
                    UPDATE customers
                    SET {assignments}
                    WHERE customer_id = %s
                    RETURNING customer_id, name, email,
                              company, created_at;
                    """,
                    (*values, customer_id)
                )

                updated_customer = cursor.fetchone()

                if updated_customer is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Customer not found."
                    )

                return updated_customer

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email already exists."
        )


# 5. Delete customer
@router.delete("/{customer_id}")
def delete_customer(customer_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM customers
                WHERE customer_id = %s
                RETURNING customer_id;
                """,
                (customer_id,)
            )

            deleted_customer = cursor.fetchone()

            if deleted_customer is None:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found."
                )

            return {
                "message": "Customer deleted successfully.",
                "customer_id": deleted_customer["customer_id"]
            }


# 6. Get complete Customer 360 profile
@router.get(
    "/{customer_id}/profile",
    response_model=Customer360Profile
)
def get_customer_profile(customer_id: int):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            # Fetch customer details
            cursor.execute(
                """
                SELECT customer_id, name, email, company, created_at
                FROM customers
                WHERE customer_id = %s;
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            if customer is None:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found."
                )

            # Fetch all support tickets
            cursor.execute(
                """
                SELECT ticket_id, customer_id, subject,
                       description, status, priority, created_at
                FROM support_tickets
                WHERE customer_id = %s
                ORDER BY created_at DESC;
                """,
                (customer_id,)
            )

            tickets = cursor.fetchall()

            # Fetch all customer interactions
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

            interactions = cursor.fetchall()

            # Combine customer, ticket and interaction data
            return {
                **customer,
                "tickets": tickets,
                "interactions": interactions
            }
