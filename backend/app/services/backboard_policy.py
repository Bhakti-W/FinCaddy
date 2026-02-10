'''
import os
import requests

# Read environment variables (set in Step 2)
BACKBOARD_API_KEY = os.getenv("BACKBOARD_API_KEY")
BACKBOARD_URL = os.getenv("BACKBOARD_URL")

if not BACKBOARD_API_KEY or not BACKBOARD_URL:
    raise RuntimeError(
        "Backboard environment variables not set. "
        "Ensure BACKBOARD_API_KEY and BACKBOARD_URL are configured."
    )

def evaluate_policy(ml: dict, cybersec: dict, compliance: dict) -> dict:
    """
    Sends ML + cybersecurity + compliance signals to Backboard
    and returns the policy decision.
    """

    payload = {
        "event_type": "policy_check",

        # ML output
        "ml": {
            "intent": ml.get("intent"),
            "confidence": ml.get("confidence")
        },

        # Cybersecurity signals
        "cybersec": cybersec,

        # Compliance flags
        "compliance": compliance
    }

    headers = {
        "Authorization": f"Bearer {BACKBOARD_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{BACKBOARD_URL}/policy/verify",
        json=payload,
        headers=headers,
        timeout=3
    )

    response.raise_for_status()
    return response.json()
'''

def evaluate_policy(ml, cybersec, compliance):
    """
    TEMPORARY stub.
    Backboard API not reachable in dev environment.
    """

    return {
        "decision": {
            "action": "ALLOW",
            "reason": "Backboard stubbed (dev mode)"
        }
    }