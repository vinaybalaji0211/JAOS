from logs.logger import logger


class ApplicationManager:

    def __init__(self):

        self.applications = {}

    def register_application(
            self,
            name,
            executable,
            status="AVAILABLE"):

        self.applications[name] = {
            "executable": executable,
            "status": status
        }

        logger.info(
            f"Application registered: {name}"
        )

    def show_applications(self):

        print("\n=== Application Manager ===\n")

        if not self.applications:

            print("No applications registered.")
            return

        for app, data in self.applications.items():

            print(app)
            print(f"  Executable : {data['executable']}")
            print(f"  Status     : {data['status']}")
            print()