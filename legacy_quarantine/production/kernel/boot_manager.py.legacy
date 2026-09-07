from logs.logger import logger


class BootManager:

    def __init__(self):

        self.steps = []

    def register_step(self, name):

        self.steps.append(name)

    def boot(self):

        print("\n========== JAOS BOOT ==========\n")

        for step in self.steps:

            print(f"✓ {step}")

            logger.info(
                f"Boot Step Completed: {step}"
            )

        print("\nJAOS Boot Completed Successfully.\n")