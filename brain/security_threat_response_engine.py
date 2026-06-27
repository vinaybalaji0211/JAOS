from logs.logger import logger


class SecurityThreatResponseEngine:

    def __init__(self):

        self.threats = []

    def report_threat(
            self,
            threat_name,
            severity):

        threat = {
            "name": threat_name,
            "severity": severity,
            "status": "DETECTED"
        }

        self.threats.append(
            threat
        )

        logger.info(
            f"Threat detected: {threat_name}"
        )

    def respond_to_threat(
            self,
            threat_name):

        for threat in self.threats:

            if threat["name"] == threat_name:

                threat["status"] = (
                    "RESPONDING"
                )

                logger.info(
                    f"Responding to: "
                    f"{threat_name}"
                )

    def resolve_threat(
            self,
            threat_name):

        for threat in self.threats:

            if threat["name"] == threat_name:

                threat["status"] = (
                    "RESOLVED"
                )

                logger.info(
                    f"Threat resolved: "
                    f"{threat_name}"
                )

    def show_threats(self):

        print(
            "\nSecurity Threat Response Engine:\n"
        )

        if not self.threats:

            print(
                "No threats detected."
            )

            return

        for threat in self.threats:

            print(
                f"Threat: "
                f"{threat['name']}"
            )

            print(
                f"Severity: "
                f"{threat['severity']}"
            )

            print(
                f"Status: "
                f"{threat['status']}"
            )

            print()