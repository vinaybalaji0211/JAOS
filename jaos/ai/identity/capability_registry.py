from jaos.ai.identity.identity_models import JAOSCapability


class CapabilityRegistry:
    """
    Registry containing all capabilities currently available
    to the running JAOS instance.
    """

    def list_capabilities(self) -> tuple[JAOSCapability, ...]:
        return (
            JAOSCapability(
                "Executive Platform",
                "Parses user intent and coordinates execution.",
            ),
            JAOSCapability(
                "Tool Platform",
                "Provides secure execution of approved tools.",
            ),
            JAOSCapability(
                "AI Platform",
                "Provides reasoning through interchangeable AI providers.",
            ),
            JAOSCapability(
                "Filesystem",
                "Read, write, copy, move, rename, delete, search and backup files.",
            ),
            JAOSCapability(
                "Diagnostics",
                "Reports platform health and operational status.",
            ),
            JAOSCapability(
                "Telemetry",
                "Collects runtime metrics for system monitoring.",
            ),
        )