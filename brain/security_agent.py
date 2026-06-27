from logs.logger import logger


class SecurityAgent:

    def __init__(self):

        self.name = "Security Agent"

        self.capabilities = [
            "threat_detection",
            "security_monitoring",
            "access_validation",
            "audit_logging",
            "risk_assessment",
            "incident_response"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "threat" in task_lower:

            result = "Threat detection task accepted."

        elif "audit" in task_lower:

            result = "Audit task accepted."

        elif "access" in task_lower:

            result = "Access validation task accepted."

        elif "risk" in task_lower:

            result = "Risk assessment task accepted."

        elif "incident" in task_lower:

            result = "Incident response task accepted."

        else:

            result = "General security task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nSecurity Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )