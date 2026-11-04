
from knowledge.document_processor import (
    extract_document,
    chunk_document
)

from knowledge.embedding_service import generate_embeddings


pdf_path = input("Enter the full path of your uploaded PDF: ")

try:
    # Step 1: Extract PDF text
    document = extract_document(pdf_path)

    # Step 2: Generate chunks
    chunks = chunk_document(
        document,
        chunk_size=1000,
        overlap=150
    )

    # Step 3: Extract chunk text
    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # Step 4: Generate embeddings
    embeddings = generate_embeddings(chunk_texts)

    print("\nEmbedding generation successful!")
    print("Document:", document["filename"])
    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))

    for index, embedding in enumerate(embeddings):

        print("\n------------------------------")
        print("Chunk ID:", chunks[index]["chunk_id"])
        print("Embedding dimensions:", len(embedding))
        print("First 5 vector values:", embedding[:5])

except Exception as error:
    print("\nEmbedding generation failed!")
    print("Error:", error)
