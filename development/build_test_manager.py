from logs.logger import logger


class BuildTestManager:

    def __init__(self):

        self.projects = {}

    def register_project(
            self,
            project_name,
            build_command,
            test_command):

        self.projects[project_name] = {
            "build": build_command,
            "test": test_command
        }

        logger.info(
            f"Build/Test profile registered: {project_name}"
        )

    def show_projects(self):

        print("\n=== Build & Test Manager ===\n")

        if not self.projects:

            print("No build profiles.")
            return

        for project, data in self.projects.items():

            print(project)
            print(f"  Build : {data['build']}")
            print(f"  Test  : {data['test']}")
            print()