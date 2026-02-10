from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from huggingface_hub import login
import numpy as np

login("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")

# =====================
# Load dataset
# =====================
dataset = load_dataset("skit-ai/skit-s2i")
dataset = dataset["train"].train_test_split(test_size=0.1)
print(dataset["train"].column_names)

# =====================
# Column names (correct for skit-s2i)
# =====================
TEXT_COL = "template"
LABEL_COL = "intent_class"

print("Dataset columns:", dataset["train"].column_names)

# =====================
# Map intent labels to IDs
# =====================
labels = list(set(dataset["train"][LABEL_COL]))
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

def encode_labels(example):
    example["label"] = label2id[example[LABEL_COL]]
    return example

dataset = dataset.map(encode_labels)

# =====================
# Tokenization
# =====================
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(
        batch[TEXT_COL],
        truncation=True,
        padding="max_length"
    )

dataset = dataset.map(tokenize, batched=True)

# =====================
# Model
# =====================
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

# =====================
# Training setup
# =====================
args = TrainingArguments(
    output_dir="./intent_model",
    eval_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    logging_dir="./logs",
    save_strategy="epoch",
    report_to="none"  # avoids wandb issues
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

# =====================
# Train & save
# =====================
trainer.train()
trainer.save_model("./intent_model")
tokenizer.save_pretrained("./intent_model")


