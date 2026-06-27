from logs.logger import logger


class SecretsManager:

    def __init__(self):

        self.secrets = {}

    def store(
            self,
            key,
            value):

        self.secrets[key] = value

        logger.info(
            f"Secret stored: {key}"
        )

    def retrieve(
            self,
            key):

        if key not in self.secrets:

            return None

        logger.info(
            f"Secret accessed: {key}"
        )

        return self.secrets[key]

    def show_keys(self):

        print("\nSecrets Manager:\n")

        if not self.secrets:

            print(
                "No secrets stored."
            )

            return

        for key in self.secrets:

            print(
                f"- {key}"
            )