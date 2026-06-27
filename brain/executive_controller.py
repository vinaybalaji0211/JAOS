from logs.logger import logger


class ExecutiveController:

    def __init__(self):

        self.system_state = "IDLE"

        self.active_goal = None

        self.active_task = None

        self.active_agent = None

    def set_goal(
            self,
            goal):

        self.active_goal = goal

        logger.info(
            f"Goal set: {goal}"
        )

    def set_task(
            self,
            task):

        self.active_task = task

        logger.info(
            f"Task set: {task}"
        )

    def assign_agent(
            self,
            agent):

        self.active_agent = agent

        logger.info(
            f"Agent assigned: {agent}"
        )

    def set_state(
            self,
            state):

        self.system_state = state

        logger.info(
            f"State changed to {state}"
        )

    def show_status(self):

        print("\nExecutive Controller:\n")

        print(
            f"State: {self.system_state}"
        )

        print(
            f"Goal: {self.active_goal}"
        )

        print(
            f"Task: {self.active_task}"
        )

        print(
            f"Agent: {self.active_agent}"
        )