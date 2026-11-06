from knowledge.vector_store import (
    get_collection,
    get_collection_count
)


try:
    collection = get_collection()

    print("\nChromaDB connection successful!")
    print("Collection name:", collection.name)
    print("Stored document chunks:", get_collection_count())

except Exception as error:
    print("\nChromaDB connection failed!")
    print("Error:", error)