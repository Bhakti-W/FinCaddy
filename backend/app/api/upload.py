from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from datetime import datetime
import uuid

# -----------------------------
# Core security & cyber modules
# -----------------------------
from app.core.hashing import generate_sha256_hash
from app.core.fingerprint import generate_audio_fingerprint, is_replay
from app.core.upload_rate import check_device_abuse
from app.core.risk_score import calculate_scam_risk
from app.core.masking import mask_sensitive_data

# -----------------------------
# Services
# -----------------------------
from app.services.compliance import check_compliance
from app.services.asr_Services import run_asr, get_intent_from_ml
from app.services.backboard_policy import evaluate_policy

router = APIRouter()

# TEMP storage for fingerprints (replace with DB later)
FINGERPRINT_DB = []


@router.post("/upload-audio")
async def upload_audio(
    request: Request,
    file: UploadFile = File(...)
):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Only audio files allowed")

    call_id = str(uuid.uuid4())
    timestamp = datetime.utcnow()

    # -----------------------------
    # 1️⃣ Read audio bytes
    # -----------------------------
    file_bytes = await file.read()

    # -----------------------------
    # 2️⃣ Integrity check (SHA-256)
    # -----------------------------
    audio_hash = generate_sha256_hash(file_bytes)

    # -----------------------------
    # 3️⃣ Audio fingerprinting (replay detection)
    # -----------------------------
    fingerprint = generate_audio_fingerprint(file_bytes)
    replay_detected = is_replay(fingerprint, FINGERPRINT_DB)
    FINGERPRINT_DB.append(fingerprint)

    # -----------------------------
    # 4️⃣ Device & upload abuse
    # -----------------------------
    device_id = request.client.host if request.client else "unknown"
    rapid_upload = check_device_abuse(device_id)

    # -----------------------------
    # 5️⃣ ASR (Whisper)
    # -----------------------------
    asr_result = run_asr(file_bytes)

    transcript = asr_result["transcript"]
    asr_confidence = asr_result["confidence"]
    asr_segments = asr_result["segments"]

    low_confidence = asr_confidence < 0.7

    # -----------------------------
    # 6️⃣ Mask sensitive data
    # -----------------------------
    masked_transcript = mask_sensitive_data(transcript)

    # -----------------------------
    # 7️⃣ Compliance checks
    # -----------------------------
    compliance_flags = check_compliance(masked_transcript)

    # -----------------------------
    # 8️⃣ Scam / risk scoring
    # -----------------------------
    scam_risk = calculate_scam_risk(
        replay=replay_detected,
        tampered=False,
        rapid_upload=rapid_upload,
        low_confidence=low_confidence
    )

    # -----------------------------
    # 9️⃣ Cybersecurity signal bundle
    # -----------------------------
    cybersec_result = {
        "integrity_ok": True,
        "replay_detected": replay_detected,
        "rapid_upload": rapid_upload,
        "low_asr_confidence": low_confidence,
        "scam_risk_score": scam_risk
    }

    # -----------------------------
    # 🔟 Intent classification (ML)
    # -----------------------------
    ml_result = get_intent_from_ml(masked_transcript)

    # -----------------------------
    # 1️⃣1️⃣ Backboard policy evaluation
    # -----------------------------
    policy_response = evaluate_policy(
        ml=ml_result,
        cybersec=cybersec_result,
        compliance=compliance_flags
    )

    action = policy_response["decision"]["action"]

    if action == "ALLOW":
        final_status = "ALLOWED"
    elif action == "FLAG":
        final_status = "FLAGGED"
    elif action == "REQUIRE_REVIEW":
        final_status = "REVIEW_REQUIRED"
    elif action == "BLOCK":
        final_status = "BLOCKED"
    else:
        final_status = "UNKNOWN"

    # -----------------------------
    # Logging (debug)
    # -----------------------------
    print(
        f"CALL={call_id} | HASH={audio_hash} | "
        f"RISK={scam_risk} | CONF={asr_confidence} | "
        f"REPLAY={replay_detected}"
    )

    # -----------------------------
    # Final response
    # -----------------------------
    return {
        "call_id": call_id,
        "timestamp": timestamp.isoformat(),

        # Backboard decision
        "final_status": final_status,

        # ASR output (Phase 1 proof)
        "transcript": transcript,
        "asr_confidence": asr_confidence,
        "asr_segments": asr_segments,

        # ML output
        "intent": ml_result["intent"],
        "intent_confidence": ml_result["confidence"],

        # Cybersecurity signals
        "cybersec_signals": cybersec_result,

        # Compliance
        "regulatory_flags": compliance_flags,

        # Safe transcript
        "masked_transcript": masked_transcript
    }