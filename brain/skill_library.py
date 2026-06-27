from logs.logger import logger


class SkillLibrary:

    def __init__(self):

        self.skills = {}

    def add_skill(
            self,
            skill_name,
            description):

        self.skills[
            skill_name
        ] = {
            "description": description
        }

        logger.info(
            f"Skill added: {skill_name}"
        )

    def get_skill(
            self,
            skill_name):

        return self.skills.get(
            skill_name
        )

    def show_skills(self):

        print(
            "\nSkill Library:\n"
        )

        if not self.skills:

            print(
                "No skills stored."
            )

            return

        for skill, details in (
                self.skills.items()):

            print(
                f"Skill: {skill}"
            )

            print(
                f"Description: "
                f"{details['description']}"
            )

            print()