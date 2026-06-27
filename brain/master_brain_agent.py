from logs.logger import logger


class MasterBrainAgent:

    def __init__(self):

        self.active_agents = []

        self.current_request = None

    def register_agent(
            self,
            agent_name):

        if agent_name not in self.active_agents:

            self.active_agents.append(
                agent_name
            )

            logger.info(
                f"Agent registered: "
                f"{agent_name}"
            )

    def receive_request(
            self,
            request):

        self.current_request = request

        logger.info(
            f"Request received: "
            f"{request}"
        )

    def show_status(self):

        print(
            "\nMaster Brain Agent:\n"
        )

        print(
            f"Current Request: "
            f"{self.current_request}"
        )

        print(
            "\nRegistered Agents:"
        )

        if not self.active_agents:

            print(
                "No agents registered."
            )

            return

        for index, agent in enumerate(
                self.active_agents,
                start=1):

            print(
                f"{index}. {agent}"
            )