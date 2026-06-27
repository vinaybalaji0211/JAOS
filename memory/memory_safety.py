from logs.logger import logger


class MemorySafety:

    BLOCKED_WORDS = [

        "password",

        "credit card",

        "bank account",

        "otp",

        "pin"

    ]

    @staticmethod
    def is_safe(memory):

        memory_lower = memory.lower()

        for word in MemorySafety.BLOCKED_WORDS:

            if word in memory_lower:

                logger.warning(

                    f"Unsafe memory blocked: {word}"

                )

                return False

        return True

    @staticmethod
    def explain(memory):

        if MemorySafety.is_safe(memory):

            print(

                "\nMemory is safe."

            )

        else:

            print(

                "\nUnsafe memory detected."

            )