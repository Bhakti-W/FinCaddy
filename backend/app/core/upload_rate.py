from collections import defaultdict
from datetime import datetime, timedelta

UPLOAD_TRACKER = defaultdict(list)

def check_device_abuse(device_id: str, max_uploads=5, window_minutes=2):
    now = datetime.utcnow()
    UPLOAD_TRACKER[device_id].append(now)

    window_start = now - timedelta(minutes=window_minutes)
    UPLOAD_TRACKER[device_id] = [
        t for t in UPLOAD_TRACKER[device_id] if t > window_start
    ]

    return len(UPLOAD_TRACKER[device_id]) > max_uploads
