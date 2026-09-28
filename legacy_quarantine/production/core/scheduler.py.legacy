from logs.logger import logger


class Scheduler:

    def __init__(self):

        self.jobs = []

    def add_job(self, job):

        self.jobs.append(job)

        logger.info(
            f"Job scheduled: {job}"
        )

    def show_jobs(self):

        print("\nScheduled Jobs:")

        if not self.jobs:

            print("No scheduled jobs.")

        else:

            for index, job in enumerate(
                    self.jobs,
                    start=1):

                print(
                    f"{index}. {job}"
                )

    def clear_jobs(self):

        self.jobs.clear()

        logger.info(
            "All jobs cleared."
        )