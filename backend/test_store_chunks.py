from knowledge.vector_store import (
    store_chunks,
    get_collection,
    get_collection_count
)


test_chunks = [
    {
        "chunk_id": 1,
        "source": "sample_enterprise_document.pdf",
        "page_number": 1,
        "text": (
            "Enterprise customer support teams should "
            "investigate repeated payment failures by "
            "checking transaction logs and payment gateway responses."
        )
    },
    {
        "chunk_id": 2,
        "source": "sample_enterprise_document.pdf",
        "page_number": 2,
        "text": (
            "When a payment transaction fails, support teams "
            "should verify the payment status before initiating "
            "a refund or retry."
        )
    }
]


try:
    initial_count = get_collection_count()

    stored_ids = store_chunks(test_chunks)

    print("\nChunks stored successfully!")
    print("New chunks stored:", len(stored_ids))
    print("Total chunks in ChromaDB:", get_collection_count())

    # Verify that the stored text can be retrieved
    collection = get_collection()

    result = collection.get(
        ids=stored_ids,
        include=["documents", "metadatas"]
    )

    print("\nRetrieved documents:")
    for document, metadata in zip(
        result["documents"],
        result["metadatas"]
    ):
        print("Text:", document)
        print("Metadata:", metadata)

    # Remove test records to keep the collection clean
    collection.delete(ids=stored_ids)

    print("\nTest records cleaned up.")
    print("Final collection count:", get_collection_count())

except Exception as error:
    print("\nChunk storage test failed!")
    print("Error:", error)


6)Create a storage test file
notepad test_store_chunks.py

**code

from knowledge.vector_store import (
    store_chunks,
    get_collection,
    get_collection_count
)


test_chunks = [
    {
        "chunk_id": 1,
        "source": "sample_enterprise_document.pdf",
        "page_number": 1,
        "text": (
            "Enterprise customer support teams should "
            "investigate repeated payment failures by "
            "checking transaction logs and payment gateway responses."
        )
    },
    {
        "chunk_id": 2,
        "source": "sample_enterprise_document.pdf",
        "page_number": 2,
        "text": (
            "When a payment transaction fails, support teams "
            "should verify the payment status before initiating "
            "a refund or retry."
        )
    }
]


try:
    initial_count = get_collection_count()

    stored_ids = store_chunks(test_chunks)

    print("\nChunks stored successfully!")
    print("New chunks stored:", len(stored_ids))
    print("Total chunks in ChromaDB:", get_collection_count())

    # Verify that the stored text can be retrieved
    collection = get_collection()

    result = collection.get(
        ids=stored_ids,
        include=["documents", "metadatas"]
    )

    print("\nRetrieved documents:")
    for document, metadata in zip(
        result["documents"],
        result["metadatas"]
    ):
        print("Text:", document)
        print("Metadata:", metadata)

    # Remove test records to keep the collection clean
    collection.delete(ids=stored_ids)

    print("\nTest records cleaned up.")
    print("Final collection count:", get_collection_count())

except Exception as error:
    print("\nChunk storage test failed!")
    print("Error:", error)





