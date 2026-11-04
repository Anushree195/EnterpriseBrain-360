from knowledge.document_processor import extract_document

pdf_path = input("Enter the full path of your uploaded PDF: ")

try:
    result = extract_document(pdf_path)

    print("\nPDF extraction successful!")
    print("Filename:", result["filename"])
    print("Pages extracted:", result["total_pages_extracted"])

    for page in result["pages"]:
        print(f"\n--- Page {page['page_number']} ---")
        print(page["text"])

except Exception as error:
    print("PDF extraction failed:", error)