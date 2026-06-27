from logs.logger import logger


class DependencyManager:

    def __init__(self):
        self.dependencies = {}

    def add_dependency(
            self,
            name,
            required_version,
            installed_version=None):

        status = "MISSING"

        if installed_version:
            if installed_version == required_version:
                status = "OK"
            else:
                status = "VERSION_CONFLICT"

        self.dependencies[name] = {
            "required_version": required_version,
            "installed_version": installed_version,
            "status": status
        }

        logger.info(f"Dependency checked: {name}")

    def show_dependencies(self):
        print("\nDependency Manager:\n")

        if not self.dependencies:
            print("No dependencies tracked.")
            return

        for name, details in self.dependencies.items():
            print(
                f"{name} | "
                f"Required: {details['required_version']} | "
                f"Installed: {details['installed_version']} | "
                f"Status: {details['status']}"
            )