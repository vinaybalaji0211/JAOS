from logs.logger import logger


class MultiAgentCoordinator:

    def __init__(self):

        self.projects = []

    def create_project(
            self,
            project_name,
            agents):

        project = {
            "project": project_name,
            "agents": agents,
            "status": "ACTIVE"
        }

        self.projects.append(
            project
        )

        logger.info(
            f"Project created: "
            f"{project_name}"
        )

    def complete_project(
            self,
            project_name):

        for project in self.projects:

            if project["project"] == project_name:

                project["status"] = (
                    "COMPLETED"
                )

    def show_projects(self):

        print(
            "\nMulti-Agent Coordinator:\n"
        )

        if not self.projects:

            print(
                "No projects."
            )

            return

        for project in self.projects:

            print(
                f"Project: "
                f"{project['project']}"
            )

            print(
                f"Agents: "
                f"{project['agents']}"
            )

            print(
                f"Status: "
                f"{project['status']}"
            )

            print()