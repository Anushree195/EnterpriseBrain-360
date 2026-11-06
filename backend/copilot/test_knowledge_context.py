from knowledge.vector_store import search_chunks


# Example question based on our test customer's ticket
query = "How can organizations optimize Azure cloud infrastructure costs?"

results = search_chunks(
    query=query,
    top_k=3
)

print("\n" + "=" * 60)
print("ENTERPRISE KNOWLEDGE RETRIEVAL")
print("=" * 60)

print(f"\nQuery: {query}")
print(f"Results found: {len(results)}")

for index, result in enumerate(results, start=1):
    print(f"\nSOURCE {index}")
    print("-" * 40)
    print(f"Document: {result['metadata']['source']}")
    print(f"Page: {result['metadata']['page_number']}")
    print(f"Distance: {result['distance']:.4f}")
    print(f"Content:\n{result['text']}")