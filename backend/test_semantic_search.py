
from knowledge.vector_store import search_chunks


queries = [
    "How can organizations optimize Azure cloud infrastructure costs?",
    "What is Azure Cost Management?",
    "How does photosynthesis work in plants?",
    "Explain horizontal and vertical scaling in cloud computing."
]

RELEVANCE_THRESHOLD = 0.65

for query in queries:

    print("\n" + "=" * 65)
    print("QUESTION:", query)

    results = search_chunks(
        query=query,
        top_k=3
    )

    if not results:
        print("No results found.")
        continue

    best_distance = results[0]["distance"]

    print("Best distance:", round(best_distance, 4))

    if best_distance <= RELEVANCE_THRESHOLD:
        print("Initial classification: RELEVANT")
    else:
        print("Initial classification: INSUFFICIENT RELEVANCE")

    for index, result in enumerate(results, start=1):
        print(
            f"Result {index}: "
            f"Distance={result['distance']:.4f}, "
            f"Page={result['metadata']['page_number']}"
        )
