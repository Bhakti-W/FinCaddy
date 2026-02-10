def detect_obligation(text):
    triggers = [
        "i will",
        "we will",
        "promise",
        "assure",
        "guarantee"
    ]
    return any(t in text.lower() for t in triggers)
