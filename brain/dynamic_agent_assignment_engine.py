from logs.logger import logger


class DynamicAgentAssignmentEngine:

    AGENT_CAPABILITY_MAP = {
        "Coding Agent": [
            "coding",
            "debugging",
            "api_generation"
        ],
        "Research Agent": [
            "research",
            "web_search",
            "fact_checking"
        ],
        "Vision Agent": [
            "vision",
            "image_analysis",
            "ocr"
        ],
        "Memory Agent": [
            "memory",
            "context",
            "retrieval"
        ],
        "Conversation Agent": [
            "conversation",
            "chat",
            "voice"
        ],
        "Security Agent": [
            "security",
            "threat_detection",
            "audit"
        ]
    }

    @staticmethod
    def assign_provider(
            provider_name,
            provider_capabilities):

        assignments = []

        for agent, required_capabilities in (
                DynamicAgentAssignmentEngine
                .AGENT_CAPABILITY_MAP
                .items()):

            matched = []

            for capability in provider_capabilities:

                if capability in required_capabilities:

                    matched.append(capability)

            if matched:

                assignments.append(
                    {
                        "provider": provider_name,
                        "agent": agent,
                        "matched_capabilities": matched
                    }
                )

        logger.info(
            f"Dynamic assignment completed for {provider_name}"
        )

        return assignments

    @staticmethod
    def show_assignments(
            provider_name,
            provider_capabilities):

        assignments = (
            DynamicAgentAssignmentEngine
            .assign_provider(
                provider_name,
                provider_capabilities
            )
        )

        print("\nDynamic Agent Assignment Engine:\n")

        if not assignments:

            print(
                "No suitable agent assignments found."
            )

            return

        for index, item in enumerate(
                assignments,
                start=1):

            print(
                f"{index}. "
                f"{item['provider']} -> "
                f"{item['agent']} | "
                f"Matched: {item['matched_capabilities']}"
            )