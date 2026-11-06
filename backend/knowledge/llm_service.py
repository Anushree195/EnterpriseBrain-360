
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
    Validate whether generated citations refer to
    actual retrieved source numbers and page numbers.
    """

    citation_pattern = r"\[Source\s+(\d+),\s*Page\s+(\d+)\]"

    found_citations = re.findall(
        citation_pattern,
        answer,
        flags=re.IGNORECASE
    )

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

    return {
        "has_citations": bool(found_citations),
        "all_citations_valid": (
            bool(found_citations)
            and not invalid_citations
        ),
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations
    }
