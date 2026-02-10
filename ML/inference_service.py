from fastapi import FastAPI
from pydantic import BaseModel

from ML.nlp.intent_infer import predict_intent
from ML.nlp.ner import extract_entities
from ML.nlp.obligation import detect_obligation

app = FastAPI(title="ML Inference Service")


class TextRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(req: TextRequest):
    intent_result = predict_intent(req.text)
    entities = extract_entities(req.text)
    obligation = detect_obligation(req.text)

    return {
        "intent": intent_result["intent"],
        "confidence": intent_result["confidence"],
        "entities": entities,
        "obligation_detected": obligation
    }

