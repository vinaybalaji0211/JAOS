from logs.logger import logger


class AutomationRulesEngine:

    def __init__(self):

        self.rules = []

    def add_rule(
            self,
            trigger,
            action):

        self.rules.append(
            {
                "trigger": trigger,
                "action": action
            }
        )

        logger.info(
            f"Automation rule added: {trigger}"
        )

    def show_rules(self):

        print(
            "\n=== Automation Rules ===\n"
        )

        if not self.rules:

            print(
                "No rules."
            )

            return

        for rule in self.rules:

            print(
                f"Trigger : {rule['trigger']}"
            )

            print(
                f"Action  : {rule['action']}"
            )

            print()