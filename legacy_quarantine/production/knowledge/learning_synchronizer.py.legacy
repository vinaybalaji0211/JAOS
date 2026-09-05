from logs.logger import logger


class LearningSynchronizer:

    def __init__(self):

        self.sync_jobs = {}

    def register_sync(
            self,
            source,
            destination,
            status="PENDING"):

        key = f"{source}->{destination}"

        self.sync_jobs[key] = {
            "source": source,
            "destination": destination,
            "status": status
        }

        logger.info(
            f"Synchronization registered: {key}"
        )

    def show_sync_jobs(self):

        print("\n=== Learning Synchronizer ===\n")

        if not self.sync_jobs:

            print("No synchronization jobs.")
            return

        for key, job in self.sync_jobs.items():

            print(key)
            print(f"  Status : {job['status']}")
            print()