from brain.threat_severity_analyzer import (
    ThreatSeverityAnalyzer
)

analyzer = (
    ThreatSeverityAnalyzer()
)

analyzer.show_analysis(
    "failed_login"
)

analyzer.show_analysis(
    "unauthorized_upgrade"
)

analyzer.show_analysis(
    "memory_tampering"
)