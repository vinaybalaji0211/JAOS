from logs.logger import logger


class ShortTermMemory:

    def __init__(self, limit=20):

        self.limit = limit

        self.memories = []

    def add(self, memory):

        self.memories.append(memory)

        if len(self.memories) > self.limit:

            self.memories.pop(0)

        logger.info(
            f"Short-term memory added: {memory}"
        )

    def get_all(self):

        return self.memories

    def show(self):

        print("\nShort-Term Memory:")

        if not self.memories:

            print("No short-term memories.")

        else:

            for index, memory in enumerate(
                    self.memories,
                    start=1):

                print(
                    f"{index}. {memory}"
                )

    def clear(self):

        self.memories.clear()

        logger.info(
            "Short-term memory cleared."
        )