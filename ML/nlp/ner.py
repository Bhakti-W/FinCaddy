import re

ACCOUNT_KEYWORDS = ["savings", "current", "credit", "wallet"]
DAY_REGEX = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"

AMOUNT_PATTERN = re.compile(
    r"(?:₹|\brupees\b|\brs\.?\b|\$)?\s*(\d+(?:\.\d{1,2})?)",
    re.IGNORECASE
)


def extract_entities(text: str) -> dict:
    text_lower = text.lower()

    # -----------------------------
    # Amounts
    # -----------------------------
    amounts = []
    for match in AMOUNT_PATTERN.finditer(text):
        amounts.append(match.group(1))

    # -----------------------------
    # Dates
    # -----------------------------
    dates = re.findall(DAY_REGEX, text_lower)

    # -----------------------------
    # Account type
    # -----------------------------
    account = None
    for acc in ACCOUNT_KEYWORDS:
        if acc in text_lower:
            account = acc
            break

    return {
        "amounts": amounts,
        "account": account,
        "dates": dates
    }




