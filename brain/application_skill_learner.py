from logs.logger import logger


class ApplicationSkillLearner:

    def __init__(self):

        self.applications = {}

    def learn_application(
            self,
            application_name,
            skill_description):

        self.applications[
            application_name
        ] = {
            "skill": skill_description,
            "status": "LEARNED"
        }

        logger.info(
            f"Learned application: "
            f"{application_name}"
        )

    def show_applications(self):

        print(
            "\nApplication Skill Learner:\n"
        )

        if not self.applications:

            print(
                "No applications learned."
            )

            return

        for app, details in (
                self.applications.items()):

            print(
                f"Application: {app}"
            )

            print(
                f"Skill: "
                f"{details['skill']}"
            )

            print(
                f"Status: "
                f"{details['status']}"
            )

            print()