
import pytest

from workflows import resolution_engine


def mock_relevant_knowledge():
    return {
        "status": "relevant_context",
        "results": [
            {
                "text": "Check the payment gateway logs for failed transactions.",
                "metadata": {
                    "source": "Payment_Guide.pdf",
                    "page_number": 12,
                    "chunk_id": "chunk_1"
                },
                "distance": 0.42
            }
        ]
    }


def test_insufficient_knowledge(monkeypatch):
    def fake_knowledge(*args, **kwargs):
        return {
            "status": "insufficient_context",
            "results": []
        }

    def unexpected_llm_call(*args, **kwargs):
        pytest.fail("Ollama should not be called.")

    monkeypatch.setattr(
        resolution_engine,
        "get_knowledge_context",
        fake_knowledge
    )

    monkeypatch.setattr(
        resolution_engine,
        "generate_answer",
        unexpected_llm_call
    )

    result = resolution_engine.generate_resolution_recommendation(
        "Payment failed",
        "Customer reported repeated payment failures."
    )

    assert result["status"] == "insufficient_context"
    assert result["sources"] == []
    assert result["citation_validation"] is None


def test_valid_citations(monkeypatch):
    monkeypatch.setattr(
        resolution_engine,
        "get_knowledge_context",
        lambda *args, **kwargs: mock_relevant_knowledge()
    )

    monkeypatch.setattr(
        resolution_engine,
        "generate_answer",
        lambda prompt: (
            "Check payment gateway logs for failed transactions. "
            "[Source 1, Page 12]"
        )
    )

    result = resolution_engine.generate_resolution_recommendation(
        "Payment failed",
        "Customer reported repeated payment failures."
    )

    assert result["status"] == "recommendation_generated"
    assert result["citation_validation"]["all_citations_valid"]
    assert len(result["sources"]) == 1


def test_invalid_citations(monkeypatch):
    monkeypatch.setattr(
        resolution_engine,
        "get_knowledge_context",
        lambda *args, **kwargs: mock_relevant_knowledge()
    )

    monkeypatch.setattr(
        resolution_engine,
        "generate_answer",
        lambda prompt: (
            "Follow the troubleshooting guide. "
            "[Source 5, Page 99]"
        )
    )

    result = resolution_engine.generate_resolution_recommendation(
        "Payment failed",
        "Customer reported repeated payment failures."
    )

    assert result["status"] == "citation_review_required"
    assert not result["citation_validation"]["all_citations_valid"]


def test_empty_subject():
    with pytest.raises(ValueError):
        resolution_engine.generate_resolution_recommendation(
            "",
            "Payment failed"
        )


def test_empty_description():
    with pytest.raises(ValueError):
        resolution_engine.generate_resolution_recommendation(
            "Payment failed",
            ""
        )
