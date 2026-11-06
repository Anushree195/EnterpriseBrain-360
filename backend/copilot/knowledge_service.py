from knowledge.vector_store import search_chunks


RELEVANCE_THRESHOLD = 0.65


def get_knowledge_context(
    query: str,
    top_k: int = 3
) -> dict:
    """
    Retrieve relevant enterprise knowledge from ChromaDB.

    Reject retrieved chunks when the best match is
    above the configured relevance threshold.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    # Step 1: Search the vector database
    results = search_chunks(
        query=query,
        top_k=top_k
    )

    # Step 2: Handle an empty knowledge base
    if not results:
        return {
            "query": query,
            "results": [],
            "best_distance": None,
            "relevance_threshold": RELEVANCE_THRESHOLD,
            "status": "insufficient_context"
        }

    # Step 3: Find the closest semantic match
    best_distance = min(
        result["distance"] for result in results
    )

    # Step 4: Reject irrelevant results
    if best_distance > RELEVANCE_THRESHOLD:
        return {
            "query": query,
            "results": [],
            "best_distance": best_distance,
            "relevance_threshold": RELEVANCE_THRESHOLD,
            "status": "insufficient_context"
        }

    # Step 5: Return relevant enterprise knowledge
    return {
        "query": query,
        "results": results,
        "best_distance": best_distance,
        "relevance_threshold": RELEVANCE_THRESHOLD,
        "status": "relevant_context"
    }