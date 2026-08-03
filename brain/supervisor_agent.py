from brain.resource_awareness_engine import ResourceAwarenessEngine
from brain.time_awareness_layer import TimeAwarenessLayer
from logs.logger import logger


class SupervisorAgent:

    def __init__(self):

        self.mode = "ACTIVE"

        self.status = "IDLE"

        self.health = "GOOD"

        self.current_goal = None

        self.current_task = None

        self.tasks_completed = 0

        self.failures = 0

    def set_goal(self, goal):

        self.current_goal = goal

        logger.info(
            f"Current goal set: {goal}"
        )

    def set_task(self, task):

        self.current_task = task

        logger.info(
            f"Current task set: {task}"
        )

    def complete_task(self):

        self.tasks_completed += 1

        self.status = "IDLE"

    def record_failure(self):

        self.failures += 1

    def success_rate(self):

        total = (
            self.tasks_completed +
            self.failures
        )

        if total == 0:

            return 100

        return round(
            self.tasks_completed * 100 / total,
            2
        )

    def show_status(self):

        resources = (
            ResourceAwarenessEngine
            .assess_resources()
        )

        time_info = (
            TimeAwarenessLayer
            .get_time_info()
        )

        print("\nSupervisor Agent:\n")

        print(
            f"Mode: {self.mode}"
        )

        print(
            f"Status: {self.status}"
        )

        print(
            f"Health: {self.health}"
        )

        print(
            f"Current Goal: {self.current_goal}"
        )

        print(
            f"Current Task: {self.current_task}"
        )

        print(
            f"Tasks Completed: {self.tasks_completed}"
        )

        print(
            f"Failures: {self.failures}"
        )

        print(
            f"Success Rate: {self.success_rate()}%"
        )

        print(
            f"Time Period: {time_info['period']}"
        )

        print(
            f"Disk Free GB: {resources['disk_free_gb']}"
        )