from logs.logger import logger


class CapabilityDiscoveryEngine:

    def __init__(self):

        self.capabilities = {}

    def register_capability(
            self,
            capability,
            available=True):

        self.capabilities[
            capability
        ] = available

        logger.info(
            f"Capability registered: "
            f"{capability}"
        )

    def discover_gap(
            self,
            required_capability):

        available = (
            self.capabilities.get(
                required_capability,
                False
            )
        )

        if available:

            return (
                "CAPABILITY_AVAILABLE"
            )

        return (
            "CAPABILITY_MISSING"
        )

    def show_capabilities(self):

        print(
            "\nCapability Discovery Engine:\n"
        )

        if not self.capabilities:

            print(
                "No capabilities registered."
            )

            return

        for capability, status in (
                self.capabilities.items()):

            print(
                f"{capability}: {status}"
            )