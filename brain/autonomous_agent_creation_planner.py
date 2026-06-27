from logs.logger import logger


class AutonomousAgentCreationPlanner:

    def __init__(self):

        self.proposals = []

    def create_proposal(
            self,
            agent_name,
            purpose):

        proposal = {
            "agent_name": agent_name,
            "purpose": purpose,
            "status": "AWAITING_APPROVAL"
        }

        self.proposals.append(
            proposal
        )

        logger.info(
            f"Agent proposal created: "
            f"{agent_name}"
        )

    def approve_proposal(
            self,
            agent_name):

        for proposal in self.proposals:

            if proposal["agent_name"] == agent_name:

                proposal["status"] = (
                    "APPROVED"
                )

    def reject_proposal(
            self,
            agent_name):

        for proposal in self.proposals:

            if proposal["agent_name"] == agent_name:

                proposal["status"] = (
                    "REJECTED"
                )

    def show_proposals(self):

        print(
            "\nAutonomous Agent Creation Planner:\n"
        )

        if not self.proposals:

            print(
                "No proposals."
            )

            return

        for proposal in self.proposals:

            print(
                f"Agent: "
                f"{proposal['agent_name']}"
            )

            print(
                f"Purpose: "
                f"{proposal['purpose']}"
            )

            print(
                f"Status: "
                f"{proposal['status']}"
            )

            print()