from logs.logger import logger


class ReflectionEngine:

    def __init__(self):

        self.reflections = []

    def reflect(
            self,
            event,
            result,
            lesson):

        reflection = {

            "event": event,

            "result": result,

            "lesson": lesson

        }

        self.reflections.append(
            reflection
        )

        logger.info(
            f"Reflection stored for {event}"
        )

    def show_reflections(self):

        print("\nReflection Engine:\n")

        if not self.reflections:

            print(
                "No reflections."
            )

            return

        for index, reflection in enumerate(
                self.reflections,
                start=1):

            print(
                f"{index}. "
                f"Event: {reflection['event']}\n"
                f"   Result: {reflection['result']}\n"
                f"   Lesson: {reflection['lesson']}\n"
            )