from logs.logger import logger


class CapabilityViewer:

    def __init__(self):

        self.capabilities = {}

    def register_capability(
            self,
            capability,
            available,
            version):

        self.capabilities[capability] = {
            "available": available,
            "version": version
        }

        logger.info(
            f"Capability registered: {capability}"
        )

    def show_capabilities(self):

        print("\n=== Capability Viewer ===\n")

        if not self.capabilities:

            print("No capabilities registered.")
            return

        for capability, data in self.capabilities.items():

            status = "AVAILABLE" if data["available"] else "NOT AVAILABLE"

            print(capability)
            print(f"  Status  : {status}")
            print(f"  Version : {data['version']}")
            print()