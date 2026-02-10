from ML.nlp.intent_infer import predict_intent
from ML.nlp.ner import extract_entities
from ML.nlp.obligation import detect_obligation
from ML.nlp.sentiment import detect_sentiment

def confidence_score(result):
    score = 0.0
    if result["obligation"]:
        score += 0.3
    if result["entities"]["amounts"]:
        score += 0.3
    if result["entities"]["dates"]:
        score += 0.2
    if result["intent"]:
        score += 0.2
    return round(score, 2)

def run_pipeline_from_text(text):
    result = {
        "transcript": text,
        "intent": predict_intent(text),
        "entities": extract_entities(text),
        "obligation": detect_obligation(text),
        "sentiment": detect_sentiment(text)
    }
    result["confidence"] = confidence_score(result)
    return result 