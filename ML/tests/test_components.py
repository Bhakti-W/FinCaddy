from ML.nlp.ner import extract_entities
from ML.nlp.obligation import detect_obligation
from ML.nlp.sentiment import detect_sentiment
from ML.nlp.intent_infer import predict_intent

text = "I will pay the EMI of 5000 by Friday"

print("Entities:", extract_entities(text))
print("Obligation:", detect_obligation(text))
print("Sentiment:", detect_sentiment(text))
print("Intent:", predict_intent(text))
