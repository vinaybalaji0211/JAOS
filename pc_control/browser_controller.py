from logs.logger import logger


class BrowserController:

    def __init__(self):

        self.sessions = {}

    def register_session(
            self,
            browser,
            website):

        self.sessions.setdefault(
            browser,
            []
        ).append(website)

        logger.info(
            f"Browser session updated: {browser}"
        )

    def show_sessions(self):

        print(
            "\n=== Browser Controller ===\n"
        )

        if not self.sessions:

            print("No browser sessions.")
            return

        for browser, websites in (
                self.sessions.items()):

            print(browser)

            for site in websites:

                print(
                    f"  - {site}"
                )

            print()