from logs.logger import logger


class ToolRecommendationEngine:

    TOOL_DATABASE = {

        "vision": [
            "Vision Module",
            "OpenCV",
            "YOLO Object Detector"
        ],

        "object_detection": [
            "YOLO Object Detector",
            "Vision Agent"
        ],

        "web_search": [
            "Web Agent",
            "Search Tool"
        ],

        "device_control": [
            "Device Control Layer",
            "Automation Engine"
        ],

        "speech": [
            "Speech Recognition Module",
            "Voice Agent"
        ],

        "voice": [
            "Text-to-Speech Module",
            "Voice Agent"
        ],

        "coding": [
            "Coding Agent",
            "OpenAI Provider"
        ],

        "research": [
            "Research Agent",
            "Perplexity Provider"
        ]

    }

    @staticmethod
    def recommend(missing_capabilities):

        recommendations = {}

        for capability in missing_capabilities:

            tools = ToolRecommendationEngine.TOOL_DATABASE.get(
                capability,
                ["No recommendation available"]
            )

            recommendations[capability] = tools

        logger.info(
            "Tool recommendations generated."
        )

        return recommendations

    @staticmethod
    def show_recommendations(
            missing_capabilities):

        recommendations = (
            ToolRecommendationEngine.recommend(
                missing_capabilities
            )
        )

        print("\nTool Recommendations:\n")

        for capability, tools in recommendations.items():

            print(
                f"Missing Capability: {capability}"
            )

            for tool in tools:

                print(
                    f"   - {tool}"
                )

            print()