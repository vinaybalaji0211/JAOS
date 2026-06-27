from logs.logger import logger


class CapabilityGapDetector:

    GAP_SOLUTIONS = {
        "vision": "Vision Module",
        "object_detection": "Object Detection System",
        "voice": "Voice System",
        "speech": "Speech Recognition Module",
        "device_control": "Device Control Layer",
        "web_search": "Web Agent",
        "file_access": "File Manager",
        "memory": "Memory Manager",
        "planning": "Planner Engine",
        "reasoning": "Reasoning Engine",
        "automation": "Automation Engine",
        "security": "Safety Decision Layer",
        "provider_selection": "Provider Router",
        "coding": "Coding Agent",
        "research": "Research Agent"
    }

    @staticmethod
    def detect_gaps(missing_capabilities):

        gaps = []

        for capability in missing_capabilities:

            suggested_system = CapabilityGapDetector.GAP_SOLUTIONS.get(
                capability,
                "Unknown system needed"
            )

            gaps.append(
                {
                    "missing_capability": capability,
                    "suggested_system": suggested_system
                }
            )

        logger.info(
            "Capability gaps detected."
        )

        return gaps

    @staticmethod
    def show_gaps(missing_capabilities):

        gaps = CapabilityGapDetector.detect_gaps(
            missing_capabilities
        )

        print("\nCapability Gap Report:")

        if not gaps:

            print("No capability gaps detected.")

        else:

            for index, gap in enumerate(
                    gaps,
                    start=1):

                print(
                    f"{index}. Missing: {gap['missing_capability']}"
                )

                print(
                    f"   Suggested System: {gap['suggested_system']}"
                )