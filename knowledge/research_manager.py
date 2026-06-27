from logs.logger import logger


class ResearchManager:

    def __init__(self):

        self.projects = {}

    def register_project(
            self,
            project_name,
            topic,
            status="ACTIVE"):

        self.projects[project_name] = {
            "topic": topic,
            "status": status
        }

        logger.info(
            f"Research project registered: {project_name}"
        )

    def show_projects(self):

        print("\n=== Research Manager ===\n")

        if not self.projects:

            print("No research projects.")
            return

        for project, data in self.projects.items():

            print(project)
            print(f"  Topic  : {data['topic']}")
            print(f"  Status : {data['status']}")
            print()