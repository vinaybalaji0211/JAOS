from logs.logger import logger


class KnowledgeCurriculumBuilder:

    def __init__(self):

        self.curriculums = {}

    def create_curriculum(
            self,
            subject,
            levels):

        self.curriculums[
            subject
        ] = levels

        logger.info(
            f"Curriculum created: "
            f"{subject}"
        )

    def show_curriculum(
            self,
            subject):

        print(
            f"\nCurriculum: {subject}\n"
        )

        curriculum = (
            self.curriculums.get(
                subject,
                {}
            )
        )

        if not curriculum:

            print(
                "No curriculum found."
            )

            return

        for level, topics in (
                curriculum.items()):

            print(
                f"{level}:"
            )

            for topic in topics:

                print(
                    f"  - {topic}"
                )

            print()