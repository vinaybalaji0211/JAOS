from logs.logger import logger


class EvidenceCollectionEngine:

    def __init__(self):

        self.evidence_store = []

    def collect(
            self,
            incident,
            evidence):

        record = {
            "incident": incident,
            "evidence": evidence
        }

        self.evidence_store.append(
            record
        )

        logger.info(
            f"Evidence collected: "
            f"{incident}"
        )

    def show_evidence(self):

        print(
            "\nEvidence Collection Engine:\n"
        )

        if not self.evidence_store:

            print(
                "No evidence collected."
            )

            return

        for item in self.evidence_store:

            print(
                f"Incident: "
                f"{item['incident']}"
            )

            print(
                f"Evidence: "
                f"{item['evidence']}"
            )

            print()