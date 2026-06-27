from logs.logger import logger


class CloudMemoryArchitecture:

    def __init__(self):

        self.memory_store = {}

    def store(
            self,
            key,
            value):

        self.memory_store[
            key
        ] = value

        logger.info(
            f"Cloud memory stored: {key}"
        )

    def retrieve(
            self,
            key):

        return self.memory_store.get(
            key
        )

    def show_memory(self):

        print(
            "\nCloud Memory Architecture:\n"
        )

        if not self.memory_store:

            print(
                "No cloud memory."
            )

            return

        for key, value in (
                self.memory_store.items()):

            print(
                f"{key}: {value}"
            )