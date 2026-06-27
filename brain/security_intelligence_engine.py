from logs.logger import logger


class SecurityIntelligenceEngine:

    def __init__(self):

        self.intelligence_records = []

    def analyze_incident(
            self,
            incident,
            assessment):

        record = {
            "incident": incident,
            "assessment": assessment
        }

        self.intelligence_records.append(
            record
        )

        logger.info(
            f"Security intelligence added: "
            f"{incident}"
        )

    def show_intelligence(self):

        print(
            "\nSecurity Intelligence Engine:\n"
        )

        if not self.intelligence_records:

            print(
                "No intelligence records."
            )

            return

        for record in (
                self.intelligence_records):

            print(
                f"Incident: "
                f"{record['incident']}"
            )

            print(
                f"Assessment: "
                f"{record['assessment']}"
            )

            print()