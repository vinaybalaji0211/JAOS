from logs.logger import logger


class VisualMemory:

    def __init__(self):

        self.memories = []

    def remember(
            self,
            memory_type,
            content):

        memory = {

            "type": memory_type,

            "content": content

        }

        self.memories.append(
            memory
        )

        logger.info(
            f"Visual memory stored: {memory_type}"
        )

    def get_memories(
            self):

        return self.memories

    def show_memories(self):

        print("\nVisual Memory:\n")

        if not self.memories:

            print(
                "No visual memories."
            )

            return

        for index, memory in enumerate(
                self.memories,
                start=1):

            print(
                f"{index}. "

                f"{memory['type']} -> "

                f"{memory['content']}"
            )