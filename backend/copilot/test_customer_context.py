
from copilot.context_service import get_customer_context


customer_id = 4

context = get_customer_context(customer_id)

if context is None:
    print("Customer not found.")

else:
    print("\nCUSTOMER PROFILE")
    print(context["customer"])

    print("\nSUPPORT TICKETS")
    for ticket in context["tickets"]:
        print(ticket)

    print("\nINTERACTION HISTORY")
    for interaction in context["interactions"]:
        print(interaction)
