
from knowledge.llm_service import validate_citations


sources = [
    {
        "source_number": 1,
        "source": "azure.pdf",
        "page_number": 31
    },
    {
        "source_number": 2,
        "source": "azure.pdf",
        "page_number": 32
    }
]


test_cases = [
    (
        "Azure costs can be monitored using Cost Management. "
        "[Source 1, Page 31]",
        "Valid citation"
    ),
    (
        "Azure budgets help monitor spending. "
        "[Source 2, Page 32]",
        "Another valid citation"
    ),
    (
        "Azure improves performance. [Source 3, Page 40]",
        "Invalid citation"
    ),
    (
        "Azure costs can be optimized using budgets.",
        "Missing citation"
    )
]


for answer, description in test_cases:

    result = validate_citations(
        answer=answer,
        sources=sources
    )

    print(f"\nTest: {description}")
    print("Answer:", answer)
    print("Validation:", result)
