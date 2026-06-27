from logs.logger import logger


class VisionAgent:

    def __init__(self):

        self.name = "Vision Agent"

        self.capabilities = [
            "image_analysis",
            "object_detection",
            "ocr",
            "screen_understanding",
            "diagram_analysis",
            "visual_reasoning"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "ocr" in task_lower:

            result = "OCR task accepted."

        elif "object" in task_lower:

            result = "Object detection task accepted."

        elif "screen" in task_lower:

            result = "Screen understanding task accepted."

        elif "diagram" in task_lower:

            result = "Diagram analysis task accepted."

        elif "image" in task_lower:

            result = "Image analysis task accepted."

        else:

            result = "General vision task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nVision Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )