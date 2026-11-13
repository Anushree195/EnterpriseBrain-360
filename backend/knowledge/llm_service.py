
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2:1b"


def generate_answer(prompt: str) -> str:
    """Generate an AI response using the local Ollama model."""

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 400
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        answer = result.get("response", "").strip()

        if not answer:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return answer

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running."
        ) from error

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Ollama took too long to generate a response."
        ) from error

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Ollama API returned an HTTP error: {error}"
        ) from error


def validate_citations(
    answer: str,
    sources: list[dict]
) -> dict:
    """
    Validate citation references and check whether
    each numbered recommendation contains a citation.

    This validates reference correctness and citation presence.
    It does not verify semantic support for each claim.
    """

    citation_pattern = re.compile(
        r"\[Source\s+(\d+),\s*Page\s+(\d+)\]",
        flags=re.IGNORECASE
    )

    found_citations = citation_pattern.findall(answer or "")

    valid_references = {
        (
            str(source["source_number"]),
            str(source["page_number"])
        )
        for source in sources
    }

    valid_citations = []
    invalid_citations = []

    for citation in found_citations:
        if citation in valid_references:
            valid_citations.append(citation)
        else:
            invalid_citations.append(citation)

    # Extract numbered recommendations.
    recommendation_match = re.search(
        r"Recommended Actions\s*:\s*(.*?)(?="
        r"Additional Information\s*:|$)",
        answer or "",
        flags=re.IGNORECASE | re.DOTALL
    )

    recommendation_items = []

    if recommendation_match:
        action_text = recommendation_match.group(1)

        recommendation_items = re.findall(
            r"(?m)^\s*\d+[.)]\s*(.+?)(?="
            r"^\s*\d+[.)]\s*|$)",
            action_text,
            flags=re.DOTALL
        )

    uncited_recommendations = []

    for index, item in enumerate(recommendation_items, start=1):
        if not citation_pattern.search(item):
            uncited_recommendations.append(index)

    has_citations = bool(found_citations)

    all_citations_valid = (
        has_citations
        and not invalid_citations
    )

    all_recommendations_cited = (
        bool(recommendation_items)
        and not uncited_recommendations
    )

    citation_review_passed = (
        all_citations_valid
        and all_recommendations_cited
    )

    return {
        "has_citations": has_citations,
        "all_citations_valid": all_citations_valid,
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations,
        "total_recommendations": len(recommendation_items),
        "uncited_recommendations": uncited_recommendations,
        "all_recommendations_cited": all_recommendations_cited,
        "citation_review_passed": citation_review_passed
    }
