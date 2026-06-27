from logs.logger import logger


class AgentLearningManager:

    def __init__(self):

        self.learning_records = {}

    def register_agent(
            self,
            agent_name):

        self.learning_records[
            agent_name
        ] = []

    def record_lesson(
            self,
            agent_name,
            lesson):

        if agent_name not in self.learning_records:

            self.learning_records[
                agent_name
            ] = []

        self.learning_records[
            agent_name
        ].append(
            lesson
        )

        logger.info(
            f"Lesson recorded for {agent_name}"
        )

    def show_learning(
            self,
            agent_name):

        print(
            f"\nLearning Record: {agent_name}\n"
        )

        lessons = self.learning_records.get(
            agent_name,
            []
        )

        if not lessons:

            print(
                "No lessons recorded."
            )

            return

        for index, lesson in enumerate(
                lessons,
                start=1):

            print(
                f"{index}. {lesson}"
            )