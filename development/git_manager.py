from logs.logger import logger


class GitManager:

    def __init__(self):

        self.repositories = {}

    def register_repository(
            self,
            name,
            path,
            branch="main"):

        self.repositories[name] = {
            "path": path,
            "branch": branch
        }

        logger.info(
            f"Repository registered: {name}"
        )

    def show_repositories(self):

        print("\n=== Git Manager ===\n")

        if not self.repositories:

            print("No repositories.")
            return

        for name, data in self.repositories.items():

            print(name)
            print(f"  Path   : {data['path']}")
            print(f"  Branch : {data['branch']}")
            print()