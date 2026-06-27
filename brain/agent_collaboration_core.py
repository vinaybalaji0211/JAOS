from logs.logger import logger


class AgentCollaborationCore:

    def __init__(self):

        self.collaborations = []

    def start_collaboration(
            self,
            goal,
            agents):

        record = {
            "goal": goal,
            "agents": agents,
            "status": "ACTIVE"
        }

        self.collaborations.append(record)

        logger.info(
            f"Collaboration started: {goal}"
        )

    def complete_collaboration(
            self,
            goal):

        for record in self.collaborations:

            if record["goal"] == goal:

                record["status"] = "COMPLETED"

                logger.info(
                    f"Collaboration completed: {goal}"
                )

    def show_collaborations(self):

        print("\nAgent Collaboration Core:\n")

        if not self.collaborations:

            print("No collaborations.")
            return

        for record in self.collaborations:

            print(f"Goal: {record['goal']}")
            print(f"Agents: {record['agents']}")
            print(f"Status: {record['status']}")
            print()