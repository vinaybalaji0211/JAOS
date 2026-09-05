from logs.logger import logger


class WindowManager:

    def __init__(self):

        self.windows = {}

    def register_window(
            self,
            window_name,
            application,
            status="OPEN"):

        self.windows[window_name] = {
            "application": application,
            "status": status
        }

        logger.info(
            f"Window registered: {window_name}"
        )

    def show_windows(self):

        print("\n=== Window Manager ===\n")

        if not self.windows:

            print("No windows registered.")
            return

        for name, data in self.windows.items():

            print(name)

            print(
                f"  Application : {data['application']}"
            )

            print(
                f"  Status      : {data['status']}"
            )

            print()