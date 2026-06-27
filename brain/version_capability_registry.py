from logs.logger import logger


class VersionCapabilityRegistry:

    def __init__(self):

        self.versions = {}

    def register_feature(
            self,
            version,
            feature):

        if version not in self.versions:

            self.versions[
                version
            ] = []

        self.versions[
            version
        ].append(
            feature
        )

        logger.info(
            f"{feature} added to {version}"
        )

    def show_version(
            self,
            version):

        print(
            f"\n{version}\n"
        )

        features = self.versions.get(
            version,
            []
        )

        if not features:

            print(
                "No registered features."
            )

            return

        for feature in features:

            print(
                f"- {feature}"
            )