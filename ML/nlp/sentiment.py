def detect_sentiment(text):
    negative_words = ["angry", "frustrated", "upset", "irritated"]
    for w in negative_words:
        if w in text.lower():
            return "negative"
    return "neutral"
