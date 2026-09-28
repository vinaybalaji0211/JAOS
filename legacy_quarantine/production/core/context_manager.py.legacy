from logs.logger import logger


class ContextManager:

    def __init__(self):

        self.context = {}

    def set_context(self, key, value):

        self.context[key] = value

        logger.info(
            f"Context updated: {key} = {value}"
        )

    def get_context(self, key):

        return self.context.get(key)

    def get_all_context(self):

        return self.context

    def show_context(self):

        print("\nCurrent Context:")

        if not self.context:

            print("No context available.")

        else:

            for key, value in self.context.items():

                print(f"{key}: {value}")

    def clear_context(self):

        self.context.clear()

        logger.info(
            "Context cleared."
        )