from pathlib import Path


class ProjectStructureValidator:

    REQUIRED_FOLDERS = [
        "core",
        "logs",
        "config",
        "memory",
        "agents",
        "tools",
        "workflow",
        "communication",
        "development",
        "knowledge",
        "security",
        "dashboard",
        "system_services",
        "engineering",
        "tests"
    ]

    def __init__(self, project_root="C:/JARVIS"):

        self.project_root = Path(project_root)

    def validate(self):

        print("\n========== PROJECT STRUCTURE VALIDATION ==========\n")

        missing = []

        for folder in self.REQUIRED_FOLDERS:

            path = self.project_root / folder

            if path.exists():

                print(f"✓ {folder}")

            else:

                print(f"✗ {folder}")

                missing.append(folder)

        print("\n=========================================\n")

        if missing:

            print("Missing folders:")

            for folder in missing:

                print(f" - {folder}")

        else:

            print("Project structure validation PASSED.")