from logs.logger import logger


class SelfCodeGenerator:

    def __init__(self):

        self.generated_code = []

    def generate(
            self,
            upgrade_name,
            code_description):

        proposal = {
            "upgrade": upgrade_name,
            "description": code_description,
            "status": "GENERATED"
        }

        self.generated_code.append(
            proposal
        )

        logger.info(
            f"Code proposal generated: "
            f"{upgrade_name}"
        )

    def show_generated_code(self):

        print(
            "\nSelf Code Generator:\n"
        )

        if not self.generated_code:

            print(
                "No code generated."
            )

            return

        for item in self.generated_code:

            print(
                f"Upgrade: "
                f"{item['upgrade']}"
            )

            print(
                f"Description: "
                f"{item['description']}"
            )

            print(
                f"Status: "
                f"{item['status']}"
            )

            print()