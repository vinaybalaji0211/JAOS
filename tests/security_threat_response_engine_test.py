from brain.security_threat_response_engine import SecurityThreatResponseEngine

engine = (
    SecurityThreatResponseEngine()
)

engine.report_threat(
    "Unauthorized Upgrade Attempt",
    "HIGH"
)

engine.report_threat(
    "Cloud Authentication Failure",
    "MEDIUM"
)

engine.respond_to_threat(
    "Unauthorized Upgrade Attempt"
)

engine.resolve_threat(
    "Cloud Authentication Failure"
)

engine.show_threats()