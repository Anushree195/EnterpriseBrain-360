
import uuid
from pathlib import Path


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status,
    Query
)

from pydantic import BaseModel, Field

from knowledge.document_processor import (
    extract_document,
    chunk_document
)

from knowledge.vector_store import (
    store_chunks,
    get_collection_count,
    search_chunks
)

from knowledge.rag_service import build_rag_prompt
from knowledge.llm_service import (
    generate_answer,
    validate_citations
)


router = APIRouter(
    prefix="/knowledge",
    tags=["Enterprise Knowledge Hub"]
)


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# Request schema for the AI question endpoint
class AskRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
        description="Question to ask the enterprise knowledge assistant"
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of relevant document chunks to retrieve"
    )


# --------------------------------------------------
# PDF DOCUMENT UPLOAD
# --------------------------------------------------

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):

    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type. Please upload a PDF."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit."
        )

    if not contents.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not contain a valid PDF signature."
        )

    document_id = str(uuid.uuid4())

    stored_filename = f"{document_id}.pdf"

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = DOCUMENTS_DIR / stored_filename

    file_path.write_bytes(contents)

    try:
        document = extract_document(str(file_path))

        if not document["pages"]:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in the PDF."
            )

        chunks = chunk_document(document)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be generated from the PDF."
            )

        stored_chunk_ids = store_chunks(chunks)

        return {
            "message": "PDF uploaded and processed successfully.",
            "document_id": document_id,
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_size_bytes": len(contents),
            "total_pages_extracted": document["total_pages_extracted"],
            "total_chunks_created": len(chunks),
            "total_chunks_stored": len(stored_chunk_ids),
            "total_chunks_in_knowledge_base": get_collection_count(),
            "status": "processed"
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        ) from error


# --------------------------------------------------
# SEMANTIC DOCUMENT SEARCH
# --------------------------------------------------

@router.get("/search")
def search_knowledge(
    query: str = Query(
        ...,
        min_length=3,
        description="Question or keywords to search in enterprise documents"
    ),
    top_k: int = Query(
        3,
        ge=1,
        le=10,
        description="Number of relevant document chunks to retrieve"
    )
):
    try:
        results = search_chunks(
            query=query,
            top_k=top_k
        )

        return {
            "query": query,
            "results_found": len(results),
            "results": [
                {
                    "content": result["text"],
                    "source": result["metadata"]["source"],
                    "page_number": result["metadata"]["page_number"],
                    "distance": result["distance"]
                }
                for result in results
            ]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Knowledge search failed: {str(error)}"
        ) from error


# --------------------------------------------------
# AI KNOWLEDGE QUESTION ANSWERING (RAG)
# --------------------------------------------------



@router.post("/ask")
def ask_knowledge(request: AskRequest):

    try:
        # Step 1: Retrieve relevant document chunks
        rag_result = build_rag_prompt(
            query=request.question,
            top_k=request.top_k
        )

        sources = rag_result["sources"]

        # Step 2: Handle empty knowledge base
        if not sources:
            return {
                "question": request.question,
                "answer": "No documents are available in the knowledge base.",
                "sources": [],
                "status": "no_documents_found",
                "citation_status": "not_available"
            }

        # Step 3: Check retrieval relevance
        relevance_threshold = 0.65

        best_distance = min(
            source["distance"] for source in sources
        )

        if best_distance > relevance_threshold:
            return {
                "question": request.question,
                "answer": (
                    "I could not find sufficiently relevant information "
                    "in the available enterprise documents to answer "
                    "this question reliably."
                ),
                "sources": [],
                "best_retrieval_distance": best_distance,
                "relevance_threshold": relevance_threshold,
                "status": "insufficient_context",
                "citation_status": "not_available"
            }

        # Step 4: Generate answer using Ollama
        answer = generate_answer(
            rag_result["prompt"]
        )

        # Step 5: Validate citations
        citation_result = validate_citations(
            answer=answer,
            sources=sources
        )

        if not citation_result["has_citations"]:
            citation_status = "missing"
        elif not citation_result["all_citations_valid"]:
            citation_status = "invalid"
        else:
            citation_status = "valid"

        # Step 6: Return response
        return {
            "question": request.question,
            "answer": answer,
            "sources": [
                {
                    "source_number": source["source_number"],
                    "filename": source["source"],
                    "page_number": source["page_number"]
                }
                for source in sources
            ],
            "citation_validation": citation_result,
            "status": "success",
            "citation_status": citation_status
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(error)}"
        ) from error
