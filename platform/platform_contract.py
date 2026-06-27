from logs.logger import logger


class PlatformContract:

    def __init__(self, name):

        self.name = name
        self.state = "CREATED"

    def initialize(self):

        self.state = "INITIALIZED"

        logger.info(
            f"{self.name} initialized."
        )

    def start(self):

        self.state = "RUNNING"

        logger.info(
            f"{self.name} started."
        )

    def pause(self):

        self.state = "PAUSED"

        logger.info(
            f"{self.name} paused."
        )

    def resume(self):

        self.state = "RUNNING"

        logger.info(
            f"{self.name} resumed."
        )

    def stop(self):

        self.state = "STOPPED"

        logger.info(
            f"{self.name} stopped."
        )

    def shutdown(self):

        self.state = "SHUTDOWN"

        logger.info(
            f"{self.name} shutdown."
        )

    def health(self):

        return {
            "platform": self.name,
            "state": self.state
        }

    def show_status(self):

        print(f"{self.name}: {self.state}")