import os
import requests
import whisper
import tempfile

ML_URL = os.getenv("ML_SERVICE_URL")

# Load Whisper once (IMPORTANT)
whisper_model = whisper.load_model("base")


def run_asr(file_bytes: bytes):
    """
    Real ASR using Whisper.
    Takes raw audio bytes.
    Returns transcript, confidence, and time-aligned segments.
    """

    # Save bytes to a temporary file (Whisper needs a file path)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(file_bytes)
        audio_path = tmp.name

    try:
        result = whisper_model.transcribe(audio_path)

        transcript = result["text"]
        language = result.get("language")

        segments = [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"]
            }
            for seg in result.get("segments", [])
        ]
        
        confidence = 0.90

        return {
            "transcript": transcript,
            "language": language,
            "segments": segments,
            "confidence": confidence
        }

    finally:
        # Clean up temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)


def get_intent_from_ml(text: str):
    """
    Sends transcript text to ML intent service.
    """
    if not ML_URL:
        raise RuntimeError("ML_SERVICE_URL is not set")

    response = requests.post(
        ML_URL,
        json={"text": text},
        timeout=3
    )
    response.raise_for_status()
    return response.json()