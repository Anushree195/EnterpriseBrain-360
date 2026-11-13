
import re

from copilot.knowledge_service import get_knowledge_context
from knowledge.llm_service import generate_answer, validate_citations


def build_resolution_prompt(
    subject: str,
    description: str,
    context: str
) -> str:
    """
    Build a concise, evidence-based prompt for support
    ticket resolution recommendations.
    """

    return f"""
You are EnterpriseBrain 360, an enterprise support
resolution assistant.

Your task is to provide concise and practical troubleshooting
recommendations for the support ticket below.

TICKET SUBJECT:
{subject}

TICKET DESCRIPTION:
{description}

RETRIEVED ENTERPRISE DOCUMENTATION:
{context}

STRICT INSTRUCTIONS:

1. Use ONLY the retrieved enterprise documentation.
2. Never invent troubleshooting procedures or technical facts.
3. Do not assume facts that are not present in the ticket.
4. Recommend only actions explicitly supported by the documentation.
5. If the documentation does not support a reliable resolution,
   clearly state that manual investigation is required.
6. Every factual recommendation must include an inline citation.
7. Use this exact citation format:
   [Source 1, Page 1]
8. Use only source numbers and page numbers provided in the
   retrieved documentation.
9. Do not invent source names, source numbers, or page numbers.
10. Do not claim that the issue has been resolved.
11. Provide a maximum of 5 troubleshooting actions.
12. Avoid repeating the same recommendation in different words.
13. Keep each recommendation short, specific, and actionable.
14. Do not request sensitive payment information from customers.
15. Never request full card numbers, CVVs, PINs, OTPs,
    passwords, authentication tokens, or payment credentials.
16. When additional information is needed, request only
    non-sensitive references such as transaction IDs,
    order references, timestamps, or provider error categories.
17. If multiple retrieved chunks describe the same action,
    consolidate them into one recommendation.

OUTPUT FORMAT:

Issue Summary:
Provide a one- or two-sentence summary of the reported issue.

Recommended Actions:
Provide up to 5 concise numbered troubleshooting actions.
Include citations for every factual recommendation.

Additional Information:
List only non-sensitive information that the support agent
should collect if required.

FORMATTING RULES:

- Use plain text.
- Do not use Markdown bold or italic formatting.
- Do not use unnecessary introductory paragraphs.
- Do not repeat the ticket description unnecessarily.
- Keep the complete response concise.

Only provide recommendations supported by the
retrieved enterprise documentation.
"""


def normalize_recommendation(answer: str) -> str:
    """
    Normalize the generated response for frontend display.
    Preserve line breaks and citation references.
    """

    if not answer:
        return ""

    # Remove Markdown bold and italic markers.
    answer = re.sub(r"\*\*(.*?)\*\*", r"\1", answer)
    answer = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", r"\1", answer)

    # Remove excessive blank lines.
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    return answer.strip()


def generate_resolution_recommendation(
    subject: str,
    description: str
) -> dict:
    """
    Generate an evidence-based support resolution
    recommendation using ChromaDB and Ollama.
    """

    if not subject or not subject.strip():
        raise ValueError("Ticket subject cannot be empty.")

    if not description or not description.strip():
        raise ValueError("Ticket description cannot be empty.")

    # Step 1: Build a search query from ticket details.
    query = f"{subject.strip()}. {description.strip()}"

    # Step 2: Retrieve relevant enterprise knowledge.
    knowledge = get_knowledge_context(
        query=query,
        top_k=3
    )

    # Step 3: Reject insufficient knowledge.
    if knowledge["status"] != "relevant_context":
        return {
            "status": "insufficient_context",
            "recommendation": (
                "The enterprise knowledge base does not contain "
                "sufficient relevant documentation to recommend "
                "a reliable resolution. Please review the ticket "
                "manually or add relevant troubleshooting documentation."
            ),
            "sources": [],
            "citation_validation": None
        }

    # Step 4: Prepare unique source references.
    context_parts = []
    sources = []

    source_lookup = {}

    for result in knowledge["results"]:
        metadata = result["metadata"]

        source_name = metadata["source"]
        page_number = metadata["page_number"]

        # Identify a source using its document and page.
        source_key = (source_name, page_number)

        if source_key not in source_lookup:
            source_number = len(sources) + 1

            source_lookup[source_key] = source_number

            sources.append({
                "source_number": source_number,
                "source": source_name,
                "page_number": page_number,
                "distance": result["distance"]
            })

            context_parts.append(
                f"""
[Source {source_number}, Page {page_number}]
Document: {source_name}

Content:
{result["text"]}
"""
            )

        else:
            # Merge additional chunks from the same document/page.
            source_number = source_lookup[source_key]

            existing_context = context_parts[source_number - 1]

            context_parts[source_number - 1] = (
                existing_context
                + "\nAdditional relevant content:\n"
                + result["text"]
            )

    context = "\n".join(context_parts)

    # Step 5: Construct the resolution prompt.
    prompt = build_resolution_prompt(
        subject=subject.strip(),
        description=description.strip(),
        context=context
    )

    # Step 6: Generate recommendation using local Ollama.
    recommendation = generate_answer(prompt)

    recommendation = normalize_recommendation(recommendation)

    # Step 7: Validate generated citations.
    citation_validation = validate_citations(
        answer=recommendation,
        sources=sources
    )

    # Step 8: Determine recommendation status.
    if citation_validation["citation_review_passed"]:
        status = "recommendation_generated"
    else:
        status = "citation_review_required"

    # Step 9: Return recommendation and evidence.
    return {
        "status": status,
        "recommendation": recommendation,
        "sources": sources,
        "citation_validation": citation_validation
    }
