from logs.logger import logger


class Scheduler:

    def __init__(self):

        self.schedules = []

    def schedule_task(
            self,
            task_name,
            schedule_time):

        self.schedules.append(
            {
                "task": task_name,
                "time": schedule_time
            }
        )

        logger.info(
            f"Scheduled: {task_name}"
        )

    def show_schedule(self):

        print(
            "\n=== Scheduler ===\n"
        )

        if not self.schedules:

            print(
                "No scheduled tasks."
            )

            return

        for item in self.schedules:

            print(
                f"{item['task']}"
            )

            print(
                f"  Time : {item['time']}"
            )

            print()