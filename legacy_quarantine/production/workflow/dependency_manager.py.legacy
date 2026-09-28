from logs.logger import logger


class DependencyManager:

    def __init__(self):

        self.dependencies = {}

    def add_dependency(
            self,
            task,
            depends_on):

        self.dependencies.setdefault(
            task,
            []
        ).append(depends_on)

        logger.info(
            f"Dependency added: "
            f"{task} -> {depends_on}"
        )

    def get_dependencies(
            self,
            task):

        return self.dependencies.get(
            task,
            []
        )

    def show_dependencies(self):

        print(
            "\n=== Dependency Manager ===\n"
        )

        if not self.dependencies:

            print(
                "No dependencies."
            )

            return

        for task, deps in (
                self.dependencies.items()):

            print(task)

            for dep in deps:

                print(
                    f"  Depends on: {dep}"
                )

            print()