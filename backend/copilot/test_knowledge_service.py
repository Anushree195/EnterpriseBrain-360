from copilot.knowledge_service import get_knowledge_context


queries = [
    "How should we investigate repeated payment failures?",
    "How can organizations optimize Azure cloud infrastructure costs?"
]


for query in queries:

    context = get_knowledge_context(query)

    print("\n" + "=" * 60)
    print("KNOWLEDGE CONTEXT TEST")
    print("=" * 60)

    print(f"\nQuestion: {query}")
    print(f"Status: {context['status']}")
    print(f"Best Distance: {context['best_distance']}")
    print(
        f"Relevance Threshold: "
        f"{context['relevance_threshold']}"
    )

    for index, result in enumerate(
        context["results"], start=1
    ):
        print(f"\nSOURCE {index}")
        print(f"Document: {result['metadata']['source']}")
        print(f"Page: {result['metadata']['page_number']}")
        print(f"Content: {result['text'][:300]}")