from logs.logger import logger


class RepositoryManager:

    def __init__(self):

        self.repositories = {}

    def add_repository(
            self,
            name,
            local_path,
            remote_url,
            branch="main"):

        self.repositories[name] = {
            "local_path": local_path,
            "remote_url": remote_url,
            "branch": branch
        }

        logger.info(
            f"Repository added: {name}"
        )

    def show_repositories(self):

        print("\n=== Repository Manager ===\n")

        if not self.repositories:

            print("No repositories.")
            return

        for name, repo in self.repositories.items():

            print(name)
            print(f"  Local  : {repo['local_path']}")
            print(f"  Remote : {repo['remote_url']}")
            print(f"  Branch : {repo['branch']}")
            print()