
import re


PRIORITY_RULES = {
    "urgent": [
        "system down",
        "production outage",
        "complete service outage",
        "security breach",
        "data loss",
        "all users affected",
        "cannot process any payments",
        "critical failure",
    ],
    "high": [
        "repeated payment failures",
        "multiple customers affected",
        "business operations blocked",
        "service unavailable",
        "unable to access account",
        "repeated failures",
        "major functionality broken",
    ],
    "low": [
        "product enquiry",
        "general enquiry",
        "general inquiry",
        "feature request",
        "product information",
        "how to use",
        "documentation request",
    ],
}


def recommend_priority(
    subject: str,
    description: str
) -> dict:
    """
    Recommend a support ticket priority using
    predefined impact-based keyword rules.

    This function does not update the database.
    """

    if not subject or not subject.strip():
        raise ValueError("Ticket subject cannot be empty.")

    if not description or not description.strip():
        raise ValueError("Ticket description cannot be empty.")

    text = f"{subject} {description}".lower()

    # Higher-impact rules take precedence.
    for priority in ["urgent", "high", "low"]:

        matched_keywords = []

        for keyword in PRIORITY_RULES[priority]:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                matched_keywords.append(keyword)

        if matched_keywords:
            return {
                "recommended_priority": priority,
                "reasons": matched_keywords,
                "recommendation_method": "keyword_rules"
            }

    # Default priority when no special rule matches.
    return {
        "recommended_priority": "medium",
        "reasons": [
            "No critical or low-impact indicators detected."
        ],
        "recommendation_method": "default_rule"
    }
