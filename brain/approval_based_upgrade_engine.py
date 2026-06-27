from logs.logger import logger


class ApprovalBasedUpgradeEngine:

    def __init__(self):

        self.requests = []

    def submit_upgrade(
            self,
            upgrade_name):

        self.requests.append(
            {
                "upgrade": upgrade_name,
                "status": "WAITING_APPROVAL"
            }
        )

        logger.info(
            f"Approval requested: "
            f"{upgrade_name}"
        )

    def approve(
            self,
            upgrade_name):

        for request in self.requests:

            if request["upgrade"] == upgrade_name:

                request["status"] = "APPROVED"

    def reject(
            self,
            upgrade_name):

        for request in self.requests:

            if request["upgrade"] == upgrade_name:

                request["status"] = "REJECTED"

    def show_requests(self):

        print(
            "\nApproval Engine:\n"
        )

        if not self.requests:

            print(
                "No approval requests."
            )

            return

        for request in self.requests:

            print(
                f"Upgrade: "
                f"{request['upgrade']}"
            )

            print(
                f"Status: "
                f"{request['status']}"
            )

            print()