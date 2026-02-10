import re

def mask_sensitive_data(text: str) -> str:

    patterns = {
        # Phone numbers (10-digit Indian)
        "phone": r"\b[6-9]\d{9}\b",

        # Aadhaar (12 digits, with or without spaces)
        "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",

        # PAN card (ABCDE1234F)
        "pan": r"\b[A-Z]{5}\d{4}[A-Z]\b",

        # Bank account numbers (9–18 digits)
        "account": r"\b\d{9,18}\b",

        # IFSC Code (SBIN0001234)
        "ifsc": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",

        # CVV (3 or 4 digits)
        "cvv": r"\b\d{3,4}\b",

        # Debit/Credit card number (16 digits)
        "card": r"\b(?:\d{4}[\s-]?){3}\d{4}\b",

        # Email address
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    }

    for label, pattern in patterns.items():
        text = re.sub(pattern, _mask_match, text)

    return text

def _mask_match(match):
    value = match.group()
    length = len(value.replace(" ", "").replace("-", ""))

    if length <= 4:
        return "*" * length

    return "*" * (length - 4) + value[-4:]
