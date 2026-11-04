
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, status


router = APIRouter(
    prefix="/knowledge",
    tags=["Enterprise Knowledge Hub"]
)

# Project root: EnterpriseBrain-360/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Uploaded PDFs are stored in the root data/documents folder
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

# Maximum upload size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):

    # 1. Validate file extension
    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 2. Validate content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type. Please upload a PDF."
        )

    # 3. Read file contents
    contents = await file.read()

    # 4. Validate empty file
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # 5. Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit."
        )

    # 6. Check PDF signature
    if not contents.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not contain a valid PDF signature."
        )

    # 7. Generate a unique server-side filename
    document_id = str(uuid.uuid4())
    stored_filename = f"{document_id}.pdf"

    # 8. Ensure the storage directory exists
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # 9. Save the PDF
    file_path = DOCUMENTS_DIR / stored_filename
    file_path.write_bytes(contents)

    # 10. Return upload details
    return {
        "message": "PDF uploaded successfully.",
        "document_id": document_id,
        "original_filename": file.filename,
        "stored_filename": stored_filename,
        "file_size_bytes": len(contents),
        "status": "uploaded"
    }
