
import re

from copilot.context_formatter import format_customer_context


def is_customer_specific_question(question: str) -> bool:
    """
    Determine whether the question explicitly requires
    customer records or customer support history.
    """

    customer_patterns = [
        r"\bcustomer\b",
        r"\bticket\b",
        r"\binteraction history\b",
        r"\bsupport history\b",
        r"\bcustomer profile\b",
        r"\bcustomer record\b",
        r"\btheir issue\b",
        r"\btheir account\b",
        r"\bthis person's\b",
        r"\bthis person\b"
    ]

    return any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in customer_patterns
    )


def build_copilot_prompt(
    customer_context: dict,
    knowledge_context: dict,
    question: str
) -> str:
    """
    Build a question-specific prompt.

    General questions receive enterprise knowledge only.
    Customer-specific questions receive customer records
    and relevant enterprise knowledge.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Determine the question type
    customer_specific = is_customer_specific_question(question)

    # Step 2: Prepare enterprise knowledge
    knowledge_results = knowledge_context.get("results", [])

    if knowledge_context.get("status") == "relevant_context":

        knowledge_lines = []

        for index, result in enumerate(
            knowledge_results,
            start=1
        ):
            source = result["metadata"]["source"]
            page = result["metadata"]["page_number"]

            knowledge_lines.append(
                f"[Source {index}, Page {page}]\n"
                f"Document: {source}\n"
                f"{result['text']}"
            )

        formatted_knowledge = "\n\n".join(knowledge_lines)

    else:
        formatted_knowledge = (
            "No sufficiently relevant enterprise knowledge "
            "was found for this question."
        )

    # Step 3: Build a general knowledge prompt
    if not customer_specific:

        prompt = f"""
You are EnterpriseBrain 360, an enterprise knowledge assistant.

Answer the user's question using ONLY the enterprise
knowledge provided below.

ENTERPRISE KNOWLEDGE
--------------------
{formatted_knowledge}

USER QUESTION
-------------
{question}

STRICT RULES
------------
1. Answer the question directly and professionally.
2. Do not mention any customer, customer profile,
   support ticket or interaction history.
3. Do not invent facts or procedures.
4. If the enterprise knowledge does not contain
   sufficient information, clearly say so.
5. Cite document-based facts using the exact format
   [Source X, Page Y].
6. Only use citations corresponding to the supplied
   enterprise knowledge.
7. Do not discuss unrelated information.

RESPONSE FORMAT
---------------
Provide:
- Direct Answer
- Key Findings
- Practical Recommendations

Do not include customer-specific sections.
"""

        return prompt.strip()

    # Step 4: Build a customer-specific prompt
    if not customer_context:
        raise ValueError(
            "Customer context is required for customer-specific questions."
        )

    formatted_customer = format_customer_context(
        customer_context
    )

    prompt = f"""
You are EnterpriseBrain 360, an enterprise customer
intelligence copilot.

Answer the user's question using the supplied customer
records and relevant enterprise knowledge.

CUSTOMER RECORDS
----------------
{formatted_customer}

ENTERPRISE KNOWLEDGE
--------------------
{formatted_knowledge}

USER QUESTION
-------------
{question}

STRICT RULES
------------
1. Customer records are the source of truth for
   customer details, tickets and interactions.

2. Enterprise documents are the source of truth for
   documented policies and procedures.

3. Only report customer facts explicitly supported
   by the supplied records.

4. Do not invent relationships between customer records
   and enterprise knowledge.

5. Never invent causes, policies or procedures.

6. If enterprise knowledge is insufficient, clearly
   state that documented guidance is unavailable.

7. Cite document-based findings using
   [Source X, Page Y].

8. Never fabricate citations.

9. Clearly distinguish recorded facts from recommendations.

RESPONSE FORMAT
---------------
1. Customer Summary
2. Current Ticket Status
3. Interaction History
4. Enterprise Knowledge Findings
5. Recommended Next Steps

Keep the response concise and factual.
"""

    return prompt.strip()
