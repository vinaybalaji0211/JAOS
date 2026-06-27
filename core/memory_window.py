from logs.logger import logger


class MemoryWindow:

    def __init__(self, limit=10):

        self.limit = limit

        self.items = []

    def add_memory(self, memory):

        self.items.append(memory)

        if len(self.items) > self.limit:

            self.items.pop(0)

        logger.info(
            f"Memory added to window: {memory}"
        )

    def get_memories(self):

        return self.items

    def show_memories(self):

        print("\nMemory Window:")

        if not self.items:

            print("No memories.")

        else:

            for index, memory in enumerate(
                    self.items,
                    start=1):

                print(
                    f"{index}. {memory}"
                )

    def clear(self):

        self.items.clear()

        logger.info(
            "Memory window cleared."
        )