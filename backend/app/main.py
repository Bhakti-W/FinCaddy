from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, UploadFile, File

# Core
from app.core.hashing import generate_sha256_hash

# API routers
from app.api.upload import router as upload_router


app = FastAPI(
    title="FinCaddy API",
    description="Audio fraud detection API",
    version="1.0.0"
)

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "Backend running"}

# -----------------------------
# Test hash endpoint
# -----------------------------
@app.post("/test-hash")
async def test_hash(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_sha256_hash(file_bytes)
    return {
        "filename": file.filename,
        "sha256_hash": file_hash
    }

# -----------------------------
# Audio upload / ASR pipeline
# -----------------------------
app.include_router(
    upload_router,
    prefix="/api",
    tags=["Audio Upload"]
)

# -----------------------------
# Debug: list registered routes
# -----------------------------
for route in app.routes:
    try:
        print(f"{route.path} -> {route.methods}")
    except Exception:
        print(route.path)

print("ML_SERVICE_URL =", os.getenv("ML_SERVICE_URL"))