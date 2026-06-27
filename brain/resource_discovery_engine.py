from logs.logger import logger


class ResourceDiscoveryEngine:

    def __init__(self):

        self.resources = {}

    def add_resource(
            self,
            subject,
            resource):

        if subject not in self.resources:

            self.resources[
                subject
            ] = []

        self.resources[
            subject
        ].append(
            resource
        )

        logger.info(
            f"Resource added: "
            f"{resource}"
        )

    def get_resources(
            self,
            subject):

        return self.resources.get(
            subject,
            []
        )

    def show_resources(self):

        print(
            "\nResource Discovery Engine:\n"
        )

        if not self.resources:

            print(
                "No resources."
            )

            return

        for subject, resources in (
                self.resources.items()):

            print(
                f"Subject: {subject}"
            )

            for resource in resources:

                print(
                    f" - {resource}"
                )

            print()