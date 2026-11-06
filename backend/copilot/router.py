
import logging

from fastapi import APIRouter, HTTPException

from schemas import CopilotRequest, CopilotResponse

from copilot.context_service import get_customer_context
from copilot.knowledge_service import get_knowledge_context
from copilot.prompt_service import build_copilot_prompt

from knowledge.llm_service import generate_answer


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/copilot",
    tags=["AI Copilot"]
)


@router.post("/ask", response_model=CopilotResponse)
def ask_copilot(request: CopilotRequest):

    try:
        # Step 1: Retrieve customer information
        customer_context = get_customer_context(
            request.customer_id
        )

        if customer_context is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found."
            )

        # Step 2: Retrieve enterprise knowledge
        knowledge_context = get_knowledge_context(
            request.question
        )

        # Step 3: Build combined prompt
        prompt = build_copilot_prompt(
            customer_context=customer_context,
            knowledge_context=knowledge_context,
            question=request.question
        )

        # Step 4: Generate AI response
        answer = generate_answer(prompt)

        # Step 5: Prepare source references
        sources = []

        if knowledge_context["status"] == "relevant_context":
            for index, result in enumerate(
                knowledge_context["results"],
                start=1
            ):
                sources.append({
                    "source_number": index,
                    "document": result["metadata"]["source"],
                    "page_number": result["metadata"]["page_number"],
                    "distance": result["distance"]
                })

        # Step 6: Return structured response
        return CopilotResponse(
            customer_id=request.customer_id,
            question=request.question,
            answer=answer,
            knowledge_status=knowledge_context["status"],
            sources=sources
        )

    except HTTPException:
        raise

    except RuntimeError as error:
        logger.exception("Copilot runtime error")

        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    except Exception as error:
        logger.exception("Copilot processing failed")

        raise HTTPException(
            status_code=500,
            detail="Copilot processing failed."
        ) from error
