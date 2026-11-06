from collections import Counter

from knowledge.vector_store import get_collection

collection = get_collection()

results = collection.get(
    include=["metadatas"]
)

source_counts = Counter(
    metadata["source"]
    for metadata in results["metadatas"]
)

print("\nDocuments stored in ChromaDB")
print("============================")

for source, count in source_counts.items():
    print(f"{source}: {count} chunks")

print("\nTotal chunks:", collection.count())