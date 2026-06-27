from logs.logger import logger


class CapabilityAwarenessEngine:

    def __init__(self):

        self.capabilities = {}

    def register(
            self,
            feature,
            version):

        self.capabilities[
            feature.lower()
        ] = version

        logger.info(
            f"Capability registered: {feature}"
        )

    def check(
            self,
            feature):

        feature = feature.lower()

        if feature in self.capabilities:

            return (
                True,
                self.capabilities[feature]
            )

        return (
            False,
            None
        )

    def show_capabilities(self):

        print(
            "\nCapability Registry:\n"
        )

        for feature, version in (
                self.capabilities.items()):

            print(
                f"{feature} -> {version}"
            )