from brain.security_intelligence_engine import SecurityIntelligenceEngine

engine = (
    SecurityIntelligenceEngine()
)

engine.analyze_incident(
    "Multiple Failed Logins",
    "Possible brute-force attempt."
)

engine.analyze_incident(
    "Unauthorized Upgrade Attempt",
    "Possible privilege escalation."
)

engine.show_intelligence()