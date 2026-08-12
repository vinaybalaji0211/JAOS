from jaos.ai.identity.identity_models import JAOSLimitation
from jaos.version import JAOS_VERSION


class LimitationRegistry:
    """
    Registry containing current operational limitations of JAOS.
    """

    def list_limitations(self) -> tuple[JAOSLimitation, ...]:
        return (
            JAOSLimitation(
                "No Direct Tool Execution by AI",
                "AI providers may reason and suggest, but tools are executed only through the Executive and Tool Platform.",
            ),
            JAOSLimitation(
                "Approval Required for Dangerous Actions",
                "Destructive or sensitive actions require explicit approval before execution.",
            ),
            JAOSLimitation(
                "Memory Platform Not Connected to This Shell",
                (
                    f"The Memory Platform is implemented and certified at "
                    f"{JAOS_VERSION}, but it is not initialized or accessible "
                    f"through the current JAOS Shell runtime."
                ),
            ),
            JAOSLimitation(
                "No Voice or Vision Yet",
                "Voice interaction and visual understanding are planned future capabilities.",
            ),
            JAOSLimitation(
                "Mock Provider Active",
                "The current AI provider is a mock provider until real providers are configured.",
            ),
        )
