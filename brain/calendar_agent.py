from logs.logger import logger


class CalendarAgent:

    def __init__(self):

        self.name = "Calendar Agent"

        self.capabilities = [
            "create_event",
            "manage_schedule",
            "track_deadlines",
            "meeting_reminders",
            "schedule_optimization",
            "calendar_summary"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "event" in task_lower:

            result = "Event creation task accepted."

        elif "deadline" in task_lower:

            result = "Deadline tracking task accepted."

        elif "meeting" in task_lower:

            result = "Meeting management task accepted."

        elif "schedule" in task_lower:

            result = "Schedule optimization task accepted."

        elif "summary" in task_lower:

            result = "Calendar summary task accepted."

        else:

            result = "General calendar task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nCalendar Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )