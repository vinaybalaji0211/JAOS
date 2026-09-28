import threading

from logs.logger import logger


class ThreadManager:

    def __init__(self):

        self.threads = []

    def run_in_thread(self, target, name):

        thread = threading.Thread(
            target=target,
            name=name
        )

        thread.start()

        self.threads.append(thread)

        logger.info(
            f"Thread started: {name}"
        )

    def show_threads(self):

        print("\nThreads:")

        if not self.threads:

            print("No active threads.")

        else:

            for thread in self.threads:

                print(
                    f"{thread.name}: alive={thread.is_alive()}"
                )

    def wait_for_all(self):

        for thread in self.threads:

            thread.join()

        logger.info(
            "All threads completed."
        )