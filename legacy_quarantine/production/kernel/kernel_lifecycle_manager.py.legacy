from logs.logger import logger


class KernelLifecycleManager:

    def __init__(self):

        self.platform_states = {}

    def register_platform(
            self,
            platform_name):

        self.platform_states[platform_name] = "STOPPED"

        logger.info(
            f"Platform registered: {platform_name}"
        )

    def start_platform(
            self,
            platform_name):

        if platform_name in self.platform_states:

            self.platform_states[platform_name] = "RUNNING"

            logger.info(
                f"Platform started: {platform_name}"
            )

    def stop_platform(
            self,
            platform_name):

        if platform_name in self.platform_states:

            self.platform_states[platform_name] = "STOPPED"

            logger.info(
                f"Platform stopped: {platform_name}"
            )

    def show_status(self):

        print("\n========== PLATFORM LIFECYCLE ==========\n")

        if not self.platform_states:

            print("No registered platforms.")
            return

        for name, state in self.platform_states.items():

            print(f"{name} : {state}")