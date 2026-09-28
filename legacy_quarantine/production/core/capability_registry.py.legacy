from logs.logger import logger


class CapabilityRegistry:

    def __init__(self):

        self.capabilities = {}

    def register_capability(self, system_name, capability):

        if system_name not in self.capabilities:

            self.capabilities[system_name] = []

        self.capabilities[system_name].append(capability)

        logger.info(
            f"Capability registered: {system_name} -> {capability}"
        )

    def get_capabilities(self):

        return self.capabilities

    def show_capabilities(self):

        print("\nCapability Registry:")

        if not self.capabilities:

            print("No capabilities registered.")

        else:

            for system, capabilities in self.capabilities.items():

                print(f"\n{system}:")

                for capability in capabilities:

                    print(f"- {capability}")