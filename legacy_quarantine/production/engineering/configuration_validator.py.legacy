from logs.logger import logger


class ConfigurationValidator:

    def __init__(self):

        self.required_keys = []

        self.config = {}

    def add_required_key(
            self,
            key):

        self.required_keys.append(key)

        logger.info(
            f"Required config key added: {key}"
        )

    def set_config(
            self,
            key,
            value):

        self.config[key] = value

    def validate(self):

        print("\n========== CONFIGURATION VALIDATOR ==========\n")

        missing = []

        for key in self.required_keys:

            if key in self.config:

                print(f"✓ {key}")

            else:

                print(f"✗ {key}")

                missing.append(key)

        print()

        if missing:

            print("Configuration validation FAILED.")

            print("Missing keys:")

            for key in missing:

                print(f" - {key}")

        else:

            print("Configuration validation PASSED.")