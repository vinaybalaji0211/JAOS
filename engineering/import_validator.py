import importlib
from logs.logger import logger


class ImportValidator:

    def __init__(self):
        self.imports = []

    def add_import(
            self,
            module_path):

        self.imports.append(module_path)

        logger.info(
            f"Import registered: {module_path}"
        )

    def validate(self):

        print("\n========== IMPORT VALIDATOR ==========\n")

        if not self.imports:
            print("No imports registered.")
            return

        failed = []

        for module_path in self.imports:

            try:
                importlib.import_module(module_path)
                print(f"✓ {module_path}")

            except Exception as error:
                print(f"✗ {module_path} -> {error}")
                failed.append(module_path)

        print()

        if failed:
            print("Import validation FAILED.")
            print("Failed imports:")

            for item in failed:
                print(f" - {item}")

        else:
            print("Import validation PASSED.")