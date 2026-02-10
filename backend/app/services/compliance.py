def check_compliance(text: str):
    text = text.lower()
    flags = []

    harassment_keywords = [
        "kill", "murder", "beat up", "stab", "shoot", "choke", "assault", "hit you",
"break your bones", "smash your face", "attack you","burn you",
"hurt your family", "kidnap", "abduct", "rape", "lynch"

    ]

    fraud_keywords = [
        "transfer money", "send money", "wire transfer",
        "upi", "bank transfer", "otp", "pin", "withdraw",
        "deposit", "refund scam", "verification charge"
    ]

    data_security_keywords = [
        "password", "passcode", "otp", "cvv", "pin",
        "account number", "ifsc", "aadhaar", "pan number",
        "card number", "credit card", "debit card"
        "send money", "transfer funds","wire money", "quick transfer",
"upi payment", "google pay", "phonepe", "paytm", "bank transfer",
"cash deposit", "instant payment", "emergency transfer"

    ]

    coercion_keywords = [
        "do it now", "immediately", "urgent", "last warning",
        "final notice", "act fast", "no time"
        "immediately", "right now", "urgent action", "act fast",
"last chance", "deadline today", "within 10 minutes",
"account will be blocked", "service will stop",
"legal action initiated", "penalty applied"

    ]

    impersonation_keywords = [
        "bank officer", "police", "customs", "income tax",
        "government", "support team", "official call","share details", "tell me the code","read the otp","confirm digits",
"send screenshot", "forward message"

    ]

    blackmail_keywords = [
        "otherwise", "or else", "we will expose",
        "leak", "report you", "complaint filed"
        "you will regret", "consequences", "last warning", "final chance",
"don’t test me", "you are finished", "we will come", "see what happens"

    ]

    if any(word in text for word in harassment_keywords):
        flags.append("Harassment / Threat")

    if any(word in text for word in fraud_keywords):
        flags.append("Potential Financial Fraud")

    if any(word in text for word in data_security_keywords):
        flags.append("Data Security Violation")

    if any(word in text for word in coercion_keywords):
        flags.append("Coercion / Pressure Tactics")

    if any(word in text for word in impersonation_keywords):
        flags.append("Impersonation Attempt")

    if any(word in text for word in blackmail_keywords):
        flags.append("Blackmail / Extortion")

    return flags
