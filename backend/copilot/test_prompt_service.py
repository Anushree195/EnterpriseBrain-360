
from copilot.context_service import get_customer_context
from copilot.knowledge_service import get_knowledge_context
from copilot.prompt_service import (
    build_copilot_prompt,
    is_customer_specific_question
)


customer_id = 4

questions = [
    "How can organizations optimize Azure cloud infrastructure costs?",
    "Summarize this customer's issue and suggest the next steps."
]

customer_context = get_customer_context(customer_id)

if customer_context is None:
    raise ValueError("Test customer not found.")

for question in questions:

    knowledge_context = get_knowledge_context(question)

    prompt = build_copilot_prompt(
        customer_context=customer_context,
        knowledge_context=knowledge_context,
        question=question
    )

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("QUESTION TYPE:",
          "Customer-specific"
          if is_customer_specific_question(question)
          else "General")
    print("=" * 70)
    print(prompt)
