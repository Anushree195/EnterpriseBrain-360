
from knowledge.document_processor import (
    extract_document,
    chunk_document
)

pdf_path = input("Enter the full path of your uploaded PDF: ")

try:
    # Step 1: Extract PDF text
    document = extract_document(pdf_path)

    # Step 2: Divide extracted text into chunks
    chunks = chunk_document(
        document,
        chunk_size=1000,
        overlap=150
    )

    print("\nText chunking successful!")
    print("Document:", document["filename"])
    print("Total chunks:", len(chunks))

    for chunk in chunks:
        print("\n------------------------------")
        print("Chunk ID:", chunk["chunk_id"])
        print("Source:", chunk["source"])
        print("Page:", chunk["page_number"])
        print("Text length:", len(chunk["text"]))
        print("Content:")
        print(chunk["text"])

except Exception as error:
    print("Chunking failed:", error)
