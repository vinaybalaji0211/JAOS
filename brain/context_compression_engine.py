from logs.logger import logger


class ContextCompressionEngine:

    @staticmethod
    def compress(context_items,
                 max_items=5):

        if len(context_items) <= max_items:

            compressed = context_items

        else:

            compressed = (
                context_items[-max_items:]
            )

        logger.info(
            "Context compressed."
        )

        return compressed

    @staticmethod
    def show_compressed(
            context_items,
            max_items=5):

        compressed = (
            ContextCompressionEngine.compress(
                context_items,
                max_items
            )
        )

        print(
            "\nContext Compression Engine:\n"
        )

        print(
            f"Original Items: "
            f"{len(context_items)}"
        )

        print(
            f"Compressed Items: "
            f"{len(compressed)}"
        )

        print("\nContext:")

        for item in compressed:

            print(
                f"- {item}"
            )