
import pytest

from workflows.priority_engine import recommend_priority


def test_urgent_priority():
    result = recommend_priority(
        "Production system down",
        "All users are unable to access the service."
    )

    assert result["recommended_priority"] == "urgent"


def test_high_priority():
    result = recommend_priority(
        "Payment failures",
        "Customer reported repeated payment failures."
    )

    assert result["recommended_priority"] == "high"


def test_medium_priority():
    result = recommend_priority(
        "Technical issue",
        "Customer reported a minor display problem."
    )

    assert result["recommended_priority"] == "medium"


def test_low_priority():
    result = recommend_priority(
        "Product enquiry",
        "Customer wants information about available features."
    )

    assert result["recommended_priority"] == "low"


def test_urgent_takes_precedence():
    result = recommend_priority(
        "Production system down",
        "A customer also submitted a feature request."
    )

    assert result["recommended_priority"] == "urgent"


def test_empty_subject():
    with pytest.raises(ValueError):
        recommend_priority("", "Payment failed")


def test_empty_description():
    with pytest.raises(ValueError):
        recommend_priority("Payment failed", "")


def test_recommendation_reason():
    result = recommend_priority(
        "Production system down",
        "All users are unable to access the service."
    )

    assert len(result["reasons"]) > 0
    assert result["recommendation_method"] == "keyword_rules"
