from logs.logger import logger


class InfrastructureIntelligenceCore:

    def __init__(self):

        self.components = {}

    def register_component(
            self,
            name,
            status):

        self.components[
            name
        ] = status

        logger.info(
            f"Infrastructure component registered: {name}"
        )

    def component_status(
            self,
            name):

        return self.components.get(
            name,
            "UNKNOWN"
        )

    def show_components(self):

        print(
            "\nInfrastructure Components\n"
        )

        if not self.components:

            print(
                "No components registered."
            )

            return

        for name, status in self.components.items():

            print(
                f"{name}: {status}"
            )