
import re


CATEGORY_KEYWORDS = {
    "payment": [
        "payment failed",
        "payment failure",
        "transaction failed",
        "transaction declined",
        "payment declined",
        "card declined",
        "payment gateway",
        "duplicate payment",
        "payment processing",
    ],
    "billing": [
        "invoice",
        "billing",
        "incorrect charge",
        "overcharged",
        "refund",
        "subscription charge",
        "charged twice",
        "billing statement",
    ],
    "account": [
        "login",
        "log in",
        "sign in",
        "password",
        "account locked",
        "account access",
        "reset password",
        "authentication",
        "two factor",
    ],
    "technical": [
        "application error",
        "server error",
        "system crash",
        "bug",
        "not loading",
        "website down",
        "api error",
        "performance issue",
        "software issue",
    ],
}


def classify_ticket(subject: str, description: str) -> dict:
    """
    Classify a support ticket using keyword matching.
    """

    if not subject or not description:
        raise ValueError(
            "Ticket subject and description cannot be empty."
        )

    text = f"{subject} {description}".lower()

    category_scores = {}
    matched_keywords = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        matches = []

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                matches.append(keyword)

        category_scores[category] = len(matches)
        matched_keywords[category] = matches

    best_category = max(
        category_scores,
        key=category_scores.get
    )

    if category_scores[best_category] == 0:
        return {
            "category": "general",
            "matched_keywords": [],
            "classification_method": "keyword_rules"
        }

    return {
        "category": best_category,
        "matched_keywords": matched_keywords[best_category],
        "classification_method": "keyword_rules"
    }
