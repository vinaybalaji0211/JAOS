from jaos.ai.identity.identity_models import JAOSIdentity


class SystemPromptBuilder:
    """
    Builds the canonical system prompt for all AI providers.
    """

    def build(self, identity: JAOSIdentity) -> str:
        lines: list[str] = [
            f"You are {identity.name}.",
            identity.codename,
            "",
            f"Version: {identity.version}",
            "",
            identity.description,
            "",
            "Current Capabilities:",
        ]

        for capability in identity.capabilities:
            lines.append(
                f"- {capability.name}: {capability.description}"
            )

        lines.append("")
        lines.append("Current Limitations:")

        for limitation in identity.limitations:
            lines.append(
                f"- {limitation.name}: {limitation.description}"
            )

        lines.extend(
            [
                "",
                "Behavior Rules:",
                "- Be accurate and truthful.",
                "- Never claim capabilities you do not have.",
                "- Use the Executive Platform for planning.",
                "- Use the Tool Platform for execution.",
                "- Dangerous actions require user approval.",
            ]
        )

        return "\n".join(lines)