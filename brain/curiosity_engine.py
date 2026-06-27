from logs.logger import logger


class CuriosityEngine:

    def __init__(self):

        self.curiosity_items = []

    def add_item(
            self,
            item,
            reason):

        self.curiosity_items.append(
            {
                "item": item,
                "reason": reason
            }
        )

        logger.info(
            f"Curiosity item added: {item}"
        )

    def show_items(self):

        print("\nCuriosity Engine:\n")

        if not self.curiosity_items:

            print(
                "No curiosity items."
            )

            return

        for index, item in enumerate(
                self.curiosity_items,
                start=1):

            print(
                f"{index}. "
                f"{item['item']} | "
                f"{item['reason']}"
            )