from pathlib import Path
from uuid import uuid4

import chromadb

from knowledge.embedding_service import generate_embeddings


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Persistent ChromaDB storage
CHROMA_DB_DIR = PROJECT_ROOT / "data" / "chroma_db"
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)


# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)


# Create or retrieve collection
document_collection = chroma_client.get_or_create_collection(
    name="enterprise_knowledge",
    metadata={
        "description": "Enterprise document chunks and embeddings"
    }
)


def get_collection():
    """Return the enterprise knowledge collection."""
    return document_collection


def get_collection_count() -> int:
    """Return the number of stored document chunks."""
    return document_collection.count()


def store_chunks(chunks: list[dict]) -> list[str]:
    """Generate embeddings and persist document chunks in ChromaDB."""

    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    # Generate vector embeddings
    embeddings = generate_embeddings(texts)

    # Generate unique IDs for each chunk
    ids = [str(uuid4()) for _ in chunks]

    # Store source and page information as metadata
    metadatas = [
        {
            "source": chunk["source"],
            "page_number": chunk["page_number"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    # Save everything to ChromaDB
    document_collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return ids



def search_chunks(query: str, top_k: int = 3) -> list[dict]:
    """Find the most relevant document chunks for a query."""

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if document_collection.count() == 0:
        return []

    # Convert the search query into an embedding
    query_embedding = generate_embeddings([query])[0]

    # Search ChromaDB for the nearest vectors
    results = document_collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, document_collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    for index in range(len(results["ids"][0])):
        matches.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return matches