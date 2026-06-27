from logs.logger import logger


class AttentionManager:

    def __init__(self):

        self.focus_item = None

        self.focus_level = "NORMAL"

    def focus_on(
            self,
            item,
            level="NORMAL"):

        self.focus_item = item

        self.focus_level = level

        logger.info(
            f"Attention focused on {item}"
        )

    def clear_focus(self):

        self.focus_item = None

        self.focus_level = "NORMAL"

        logger.info(
            "Attention cleared."
        )

    def show_focus(self):

        print("\nAttention Manager:\n")

        print(
            f"Focus Item: {self.focus_item}"
        )

        print(
            f"Focus Level: {self.focus_level}"
        )