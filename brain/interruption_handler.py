from logs.logger import logger


class InterruptionHandler:

    def __init__(self):

        self.current_task = None
        self.paused_task = None
        self.interruption_source = None
        self.interrupted = False

    def start_task(
            self,
            task):

        self.current_task = task

        logger.info(
            f"Task started: {task}"
        )

    def interrupt(
            self,
            source):

        self.paused_task = self.current_task
        self.interruption_source = source
        self.interrupted = True

        logger.info(
            f"Interrupted by: {source}"
        )

    def resume(self):

        if self.paused_task:

            self.current_task = self.paused_task
            self.paused_task = None
            self.interruption_source = None
            self.interrupted = False

            logger.info(
                "Task resumed."
            )

    def show_status(self):

        print("\nInterruption Handler:\n")

        print(
            f"Current Task: {self.current_task}"
        )

        print(
            f"Paused Task: {self.paused_task}"
        )

        print(
            f"Interruption Source: {self.interruption_source}"
        )

        print(
            f"Interrupted: {self.interrupted}"
        )