from logs.logger import logger


class ThreatSeverityAnalyzer:

    def __init__(self):

        self.rules = {
            "failed_login": "LOW",
            "multiple_failed_logins": "MEDIUM",
            "unauthorized_upgrade": "HIGH",
            "memory_tampering": "CRITICAL",
            "cloud_breach": "CRITICAL"
        }

    def analyze(
            self,
            threat_type):

        severity = self.rules.get(
            threat_type,
            "UNKNOWN"
        )

        logger.info(
            f"Threat analyzed: "
            f"{threat_type}"
        )

        return severity

    def show_analysis(
            self,
            threat_type):

        severity = self.analyze(
            threat_type
        )

        print(
            "\nThreat Severity Analysis:\n"
        )

        print(
            f"Threat: {threat_type}"
        )

        print(
            f"Severity: {severity}"
        )