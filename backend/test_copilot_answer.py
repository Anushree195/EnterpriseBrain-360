from copilot.context_service import get_customer_context
from copilot.knowledge_service import get_knowledge_context
from copilot.prompt_service import build_copilot_prompt

from knowledge.llm_service import generate_answer


customer_id = 4

question = (
    "Summarize this customer's issue and suggest "
    "the next steps."
)

# Step 1: Retrieve customer context
customer_context = get_customer_context(customer_id)

if customer_context is None:
    raise ValueError("Customer not found.")

# Step 2: Retrieve relevant enterprise knowledge
knowledge_context = get_knowledge_context(question)

# Step 3: Build the combined prompt
prompt = build_copilot_prompt(
    customer_context=customer_context,
    knowledge_context=knowledge_context,
    question=question
)

# Step 4: Generate the AI response
answer = generate_answer(prompt)

# Step 5: Display the result
print("\n" + "=" * 60)
print("ENTERPRISEBRAIN 360 — AI COPILOT")
print("=" * 60)

print(f"\nCustomer ID: {customer_id}")
print(f"Question: {question}")

print("\nAI COPILOT RESPONSE")
print("-" * 60)
print(answer)

print("\nKNOWLEDGE STATUS")
print(knowledge_context["status"])