from logs.logger import logger


class MemoryConsolidation:

    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = []
        self.noise = []

    def add_short_term(self, item, important=False):
        memory = {
            "item": item,
            "important": important
        }

        self.short_term_memory.append(memory)

        logger.info("Short-term memory added.")

    def consolidate(self):
        for memory in self.short_term_memory:
            if memory["important"]:
                self.long_term_memory.append(
                    memory["item"]
                )
            else:
                self.noise.append(
                    memory["item"]
                )

        self.short_term_memory = []

        logger.info("Memory consolidation completed.")

    def show_memory(self):
        print("\nMemory Consolidation:\n")
        print(f"Short Term: {self.short_term_memory}")
        print(f"Long Term: {self.long_term_memory}")
        print(f"Noise: {self.noise}")