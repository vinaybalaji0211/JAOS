from logs.logger import logger


class IntelligentResourceOrchestrator:

    def __init__(self):

        self.resources = {}

    def register_resource(
            self,
            resource_name,
            resource_type,
            status):

        self.resources[resource_name] = {
            "type": resource_type,
            "status": status
        }

        logger.info(
            f"Registered resource: {resource_name}"
        )

    def get_resource(
            self,
            resource_name):

        return self.resources.get(resource_name)

    def show_resources(self):

        print("\n=== Intelligent Resource Orchestrator ===\n")

        if not self.resources:

            print("No resources registered.")
            return

        for name, data in self.resources.items():

            print(
                f"{name}"
            )

            print(
                f"  Type   : {data['type']}"
            )

            print(
                f"  Status : {data['status']}"
            )

            print()