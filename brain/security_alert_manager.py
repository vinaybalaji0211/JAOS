from logs.logger import logger


class SecurityAlertManager:

    def __init__(self):

        self.alerts = []

    def create_alert(
            self,
            threat_name,
            severity):

        alert = {
            "threat": threat_name,
            "severity": severity,
            "status": "ACTIVE"
        }

        self.alerts.append(
            alert
        )

        logger.info(
            f"Alert created: {threat_name}"
        )

    def acknowledge_alert(
            self,
            threat_name):

        for alert in self.alerts:

            if alert["threat"] == threat_name:

                alert["status"] = (
                    "ACKNOWLEDGED"
                )

    def show_alerts(self):

        print(
            "\nSecurity Alert Manager:\n"
        )

        if not self.alerts:

            print(
                "No alerts."
            )

            return

        for alert in self.alerts:

            print(
                f"Threat: "
                f"{alert['threat']}"
            )

            print(
                f"Severity: "
                f"{alert['severity']}"
            )

            print(
                f"Status: "
                f"{alert['status']}"
            )

            print()