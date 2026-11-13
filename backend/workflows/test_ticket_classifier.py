
import pytest

from workflows.ticket_classifier import classify_ticket


def test_payment_ticket():
    result = classify_ticket(
        "Payment failed",
        "Customer reported repeated payment failures."
    )

    assert result["category"] == "payment"


def test_billing_ticket():
    result = classify_ticket(
        "Incorrect invoice",
        "Customer was charged twice."
    )

    assert result["category"] == "billing"


def test_account_ticket():
    result = classify_ticket(
        "Unable to login",
        "Customer needs to reset password."
    )

    assert result["category"] == "account"


def test_technical_ticket():
    result = classify_ticket(
        "Application error",
        "The application crashes when opening."
    )

    assert result["category"] == "technical"


def test_general_ticket():
    result = classify_ticket(
        "Product enquiry",
        "I would like more information about your services."
    )

    assert result["category"] == "general"


def test_empty_subject():
    with pytest.raises(ValueError):
        classify_ticket("", "Payment failed")


def test_empty_description():
    with pytest.raises(ValueError):
        classify_ticket("Payment failed", "")
