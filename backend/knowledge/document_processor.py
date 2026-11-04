
import re
from pathlib import Path

import pymupdf


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Returns a list containing page numbers and extracted text.
    """

    extracted_pages = []

    try:
        with pymupdf.open(file_path) as pdf_document:

            for page_number, page in enumerate(pdf_document, start=1):

                text = page.get_text("text")
                cleaned_text = clean_text(text)

                if cleaned_text:
                    extracted_pages.append({
                        "page_number": page_number,
                        "text": cleaned_text
                    })

    except Exception as error:
        raise ValueError(
            f"Could not extract text from PDF: {error}"
        ) from error

    return extracted_pages


def clean_text(text: str) -> str:
    """
    Remove unnecessary whitespace and formatting noise.
    """

    # Replace multiple spaces and tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize repeated line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading and trailing whitespace
    return text.strip()


def extract_document(file_path: str) -> dict:
    """
    Extract and summarize the contents of a PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("PDF file not found.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    pages = extract_text_from_pdf(str(path))

    return {
        "filename": path.name,
        "total_pages_extracted": len(pages),
        "pages": pages
    }


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[str]:
    """
    Divide text into overlapping chunks without splitting words.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be non-negative and smaller than chunk size."
        )

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        # Move the end to a word boundary
        if end < text_length:
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # Calculate the next starting position with overlap
        next_start = max(start + 1, end - overlap)

        # Move forward until the next word boundary
        while next_start < end and not text[next_start - 1].isspace():
            next_start += 1

        start = next_start

    return chunks


def chunk_document(
    document: dict,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[dict]:
    """
    Split an extracted document into chunks.

    Preserve source filename and PDF page number
    for future RAG citations.
    """

    all_chunks = []
    chunk_id = 1

    for page in document["pages"]:

        page_chunks = chunk_text(
            page["text"],
            chunk_size,
            overlap
        )

        for chunk in page_chunks:

            all_chunks.append({
                "chunk_id": chunk_id,
                "source": document["filename"],
                "page_number": page["page_number"],
                "text": chunk
            })

            chunk_id += 1

    return all_chunks
