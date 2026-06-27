import time

from logs.logger import logger


class PerformanceMonitor:

    def __init__(self):

        self.start_time = None

        self.end_time = None

    def start_timer(self):

        self.start_time = time.time()

        logger.info(
            "Performance timer started."
        )

    def stop_timer(self):

        self.end_time = time.time()

        logger.info(
            "Performance timer stopped."
        )

    def get_duration(self):

        if self.start_time is None or self.end_time is None:

            return None

        return self.end_time - self.start_time

    def show_duration(self):

        duration = self.get_duration()

        if duration is None:

            print("Performance duration not available.")

        else:

            print(
                f"Execution Time: {duration:.4f} seconds"
            )