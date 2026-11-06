
from copilot.context_service import get_customer_context
from copilot.context_formatter import format_customer_context


customer_id = 4

# Retrieve data from PostgreSQL
context = get_customer_context(customer_id)

if context is None:
    print("Customer not found.")

else:
    # Convert database records into structured text
    formatted_context = format_customer_context(context)

    print("\n" + "=" * 60)
    print("FORMATTED CUSTOMER CONTEXT")
    print("=" * 60)

    print(formatted_context)
