from logs.logger import logger


class AgentTrainingManager:

    def __init__(self):

        self.training_records = {}

    def start_training(
            self,
            agent_name,
            curriculum):

        self.training_records[
            agent_name
        ] = {
            "curriculum": curriculum,
            "progress": 0
        }

        logger.info(
            f"Training started: "
            f"{agent_name}"
        )

    def update_progress(
            self,
            agent_name,
            progress):

        if agent_name in (
                self.training_records):

            self.training_records[
                agent_name
            ]["progress"] = progress

    def show_training(self):

        print(
            "\nAgent Training Manager:\n"
        )

        if not self.training_records:

            print(
                "No training records."
            )

            return

        for agent, record in (
                self.training_records.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                f"Curriculum: "
                f"{record['curriculum']}"
            )

            print(
                f"Progress: "
                f"{record['progress']}%"
            )

            print()