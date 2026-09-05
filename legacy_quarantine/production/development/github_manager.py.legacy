from logs.logger import logger


class GitHubManager:

    def __init__(self):

        self.repositories = {}

    def register_repository(
            self,
            name,
            url,
            status="CONNECTED"):

        self.repositories[name] = {
            "url": url,
            "status": status
        }

        logger.info(
            f"GitHub repository registered: {name}"
        )

    def show_repositories(self):

        print("\n=== GitHub Manager ===\n")

        if not self.repositories:

            print("No GitHub repositories.")
            return

        for name, data in self.repositories.items():

            print(name)
            print(f"  URL    : {data['url']}")
            print(f"  Status : {data['status']}")
            print()