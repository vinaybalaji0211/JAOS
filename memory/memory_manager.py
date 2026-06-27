from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from logs.logger import logger


class MemoryManager:

    def __init__(self):

        self.short_term = ShortTermMemory()

    def remember_short_term(self, memory):

        self.short_term.add(memory)

        logger.info(
            f"Memory manager stored short-term memory: {memory}"
        )

    def remember_long_term(self, memory):

        LongTermMemory.add(memory)

        logger.info(
            f"Memory manager stored long-term memory: {memory}"
        )

    def show_short_term(self):

        self.short_term.show()

    def show_long_term(self):

        LongTermMemory.show()

    def show_all(self):

        self.show_short_term()

        self.show_long_term()