from jaos.ai.identity.identity_models import JAOSLimitation


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
                "No Long-Term Memory Yet",
                "Long-term memory is planned but not yet fully implemented.",
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