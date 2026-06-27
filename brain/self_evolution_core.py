from logs.logger import logger


class SelfEvolutionCore:

    def __init__(self):

        self.evolution_enabled = True

        self.approval_required = True

        self.pending_upgrades = []

    def propose_upgrade(
            self,
            upgrade_name,
            reason):

        proposal = {
            "upgrade": upgrade_name,
            "reason": reason,
            "status": "PENDING_APPROVAL"
        }

        self.pending_upgrades.append(
            proposal
        )

        logger.info(
            f"Upgrade proposed: {upgrade_name}"
        )

    def approve_upgrade(
            self,
            upgrade_name):

        for upgrade in self.pending_upgrades:

            if upgrade["upgrade"] == upgrade_name:

                upgrade["status"] = "APPROVED"

                logger.info(
                    f"Upgrade approved: {upgrade_name}"
                )

    def reject_upgrade(
            self,
            upgrade_name):

        for upgrade in self.pending_upgrades:

            if upgrade["upgrade"] == upgrade_name:

                upgrade["status"] = "REJECTED"

                logger.info(
                    f"Upgrade rejected: {upgrade_name}"
                )

    def show_status(self):

        print(
            "\nSelf-Evolution Core:\n"
        )

        print(
            f"Evolution Enabled: "
            f"{self.evolution_enabled}"
        )

        print(
            f"Approval Required: "
            f"{self.approval_required}"
        )

        print(
            "\nPending Upgrades:\n"
        )

        if not self.pending_upgrades:

            print(
                "No pending upgrades."
            )

            return

        for upgrade in self.pending_upgrades:

            print(
                f"Upgrade: "
                f"{upgrade['upgrade']}"
            )

            print(
                f"Reason: "
                f"{upgrade['reason']}"
            )

            print(
                f"Status: "
                f"{upgrade['status']}"
            )

            print()