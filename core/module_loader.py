from logs.logger import logger


class ModuleLoader:

    def __init__(self):

        self.modules = []

    def load_module(self, module_name):

        self.modules.append(module_name)

        logger.info(f"Module loaded: {module_name}")

    def show_modules(self):

        print("Loaded Modules:")

        for module in self.modules:

            print("-", module)