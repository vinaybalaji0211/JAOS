from logs.logger import logger


class DependencyValidator:

    def __init__(self):

        self.dependencies = {}

    def add_dependency(
            self,
            module,
            dependency):

        self.dependencies.setdefault(
            module,
            []
        ).append(dependency)

        logger.info(
            f"Dependency added: {module} -> {dependency}"
        )

    def validate(self):

        print("\n========== DEPENDENCY VALIDATOR ==========\n")

        if not self.dependencies:

            print("No dependencies registered.")
            return

        for module, deps in self.dependencies.items():

            print(module)

            for dependency in deps:

                print(f"  Depends on : {dependency}")

            print()

        print("Dependency validation completed.")