from logs.logger import logger


class DynamicModuleLoader:

    def __init__(self):

        self.modules = {}

    def load(
            self,
            module_name):

        self.modules[module_name] = "ACTIVE"

        logger.info(
            f"Module loaded: {module_name}"
        )

    def unload(
            self,
            module_name):

        if module_name in self.modules:

            self.modules[module_name] = "INACTIVE"

            logger.info(
                f"Module unloaded: {module_name}"
            )

    def reload(
            self,
            module_name):

        self.modules[module_name] = "ACTIVE"

        logger.info(
            f"Module reloaded: {module_name}"
        )

    def show_modules(self):

        print("\nDynamic Module Loader:\n")

        if not self.modules:

            print(
                "No modules loaded."
            )

            return

        for module, state in self.modules.items():

            print(
                f"{module}: {state}"
            )