from logs.logger import logger


class ReflectiveReasoningEngine:

    def __init__(self):

        self.reflections = []

    def reflect(
            self,
            reasoning_goal,
            strengths,
            weaknesses,
            improvement):

        reflection = {
            "goal": reasoning_goal,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement": improvement
        }

        self.reflections.append(
            reflection
        )

        logger.info(
            f"Reflection completed: "
            f"{reasoning_goal}"
        )

    def show_reflections(self):

        print(
            "\nReflective Reasoning Engine:\n"
        )

        if not self.reflections:

            print(
                "No reflections."
            )

            return

        for reflection in self.reflections:

            print(
                f"Goal: "
                f"{reflection['goal']}"
            )

            print(
                f"Strengths: "
                f"{reflection['strengths']}"
            )

            print(
                f"Weaknesses: "
                f"{reflection['weaknesses']}"
            )

            print(
                f"Improvement: "
                f"{reflection['improvement']}"
            )

            print()