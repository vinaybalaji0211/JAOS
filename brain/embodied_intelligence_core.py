from logs.logger import logger


class EmbodiedIntelligenceCore:

    def __init__(self):

        self.skills = []

        self.active_environment = None

    def register_skill(
            self,
            skill):

        self.skills.append(
            skill
        )

        logger.info(
            f"Skill registered: {skill}"
        )

    def set_environment(
            self,
            environment):

        self.active_environment = (
            environment
        )

        logger.info(
            f"Environment set: {environment}"
        )

    def show_status(self):

        print(
            "\nEmbodied Intelligence Core:\n"
        )

        print(
            f"Environment: "
            f"{self.active_environment}"
        )

        print(
            "\nSkills:\n"
        )

        if not self.skills:

            print(
                "No skills loaded."
            )

            return

        for skill in self.skills:

            print(
                f"- {skill}"
            )