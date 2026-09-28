from logs.logger import logger


class ActionQueue:

    def __init__(self):

        self.queue = []

    def add_action(self, action):

        self.queue.append(action)

        logger.info(
            f"Action queued: {action}"
        )

    def execute_next(self):

        if not self.queue:

            print("No actions in queue.")

            return

        action = self.queue.pop(0)

        logger.info(
            f"Action executed: {action}"
        )

        print(
            f"Executing: {action}"
        )

    def show_queue(self):

        print("\nAction Queue:")

        if not self.queue:

            print("Queue is empty.")

        else:

            for index, action in enumerate(
                    self.queue,
                    start=1):

                print(
                    f"{index}. {action}"
                )

    def clear_queue(self):

        self.queue.clear()

        logger.info(
            "Action queue cleared."
        )
        