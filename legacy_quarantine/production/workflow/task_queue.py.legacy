from logs.logger import logger


class TaskQueue:

    def __init__(self):

        self.queue = []

    def add_task(
            self,
            task_name,
            priority):

        self.queue.append(
            {
                "task": task_name,
                "priority": priority
            }
        )

        priority_order = {
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        self.queue.sort(
            key=lambda item:
            priority_order.get(
                item["priority"],
                99
            )
        )

        logger.info(
            f"Queued task: {task_name}"
        )

    def next_task(self):

        if not self.queue:

            return None

        return self.queue.pop(0)

    def show_queue(self):

        print("\n=== Task Queue ===\n")

        if not self.queue:

            print("Queue empty.")
            return

        for task in self.queue:

            print(
                f"{task['task']} "
                f"({task['priority']})"
            )