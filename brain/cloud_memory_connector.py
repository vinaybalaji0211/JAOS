from logs.logger import logger


class CloudMemoryConnector:

    def __init__(self):

        self.provider = None

        self.connected = False

    def connect(
            self,
            provider_name):

        self.provider = provider_name

        self.connected = True

        logger.info(
            f"Connected to cloud provider: "
            f"{provider_name}"
        )

    def disconnect(self):

        logger.info(
            f"Disconnected from: "
            f"{self.provider}"
        )

        self.provider = None

        self.connected = False

    def status(self):

        print(
            "\nCloud Memory Connector:\n"
        )

        print(
            f"Provider: "
            f"{self.provider}"
        )

        print(
            f"Connected: "
            f"{self.connected}"
        )