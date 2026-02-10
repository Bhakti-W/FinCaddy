def calculate_scam_risk(
    replay: bool,
    tampered: bool,
    rapid_upload: bool,
    low_confidence: bool
):
    score = 0

    if replay:
        score += 40
    if tampered:
        score += 30
    if rapid_upload:
        score += 20
    if low_confidence:
        score += 90
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"
