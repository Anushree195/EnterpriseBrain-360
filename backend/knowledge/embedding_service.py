
from fastembed import TextEmbedding


# Lightweight embedding model
MODEL_NAME = "BAAI/bge-small-en-v1.5"


# Initialize the embedding model
embedding_model = TextEmbedding(
    model_name=MODEL_NAME
)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate numerical embeddings for a list of text chunks.

    Each text is converted into a vector of floating-point numbers.
    """

    if not texts:
        return []

    embeddings = embedding_model.embed(texts)

    return [
        embedding.tolist()
        for embedding in embeddings
    ]


def generate_single_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single text.
    """

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    embeddings = generate_embeddings([text])

    return embeddings[0]
