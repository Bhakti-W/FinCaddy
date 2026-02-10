import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -----------------------------
# Load the BEST checkpoint
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "intent_model", "checkpoint-2350")
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR, local_files_only=True
)

model.eval()  # IMPORTANT


def predict_intent(text: str):
    """
    Predict intent + confidence from text
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=-1)

    confidence, pred_id = torch.max(probs, dim=-1)

    intent = model.config.id2label[pred_id.item()]

    return {
        "intent": intent,
        "confidence": round(confidence.item(), 4)
    }


