from logs.logger import logger


class SkillMarketplace:

    def __init__(self):

        self.skills = {}

    def add_skill(
            self,
            skill_name,
            version):

        self.skills[skill_name] = {
            "version": version,
            "status": "INSTALLED"
        }

        logger.info(
            f"Skill installed: {skill_name}"
        )

    def remove_skill(
            self,
            skill_name):

        if skill_name in self.skills:

            self.skills[skill_name][
                "status"
            ] = "REMOVED"

            logger.info(
                f"Skill removed: {skill_name}"
            )

    def show_skills(self):

        print("\nSkill Marketplace:\n")

        if not self.skills:

            print(
                "No skills installed."
            )

            return

        for skill, details in self.skills.items():

            print(
                f"{skill} | "
                f"Version {details['version']} | "
                f"{details['status']}"
            )