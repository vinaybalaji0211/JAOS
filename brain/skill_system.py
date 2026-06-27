from logs.logger import logger


class SkillSystem:

    def __init__(self):

        self.skills = {}

    def install_skill(

            self,

            name,

            description):

        self.skills[name] = {

            "description": description,

            "status": "ACTIVE"

        }

        logger.info(

            f"Skill installed: {name}"

        )

    def uninstall_skill(

            self,

            name):

        if name in self.skills:

            del self.skills[name]

            logger.info(

                f"Skill removed: {name}"

            )

    def get_skills(self):

        return self.skills

    def show_skills(self):

        print("\nInstalled Skills:")

        if not self.skills:

            print("No skills installed.")

        else:

            for name, details in self.skills.items():

                print(

                    f"{name}: "

                    f"{details['description']} "

                    f"({details['status']})"

                )