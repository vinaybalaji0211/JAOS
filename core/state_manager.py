from logs.logger import logger


class StateManager:

    def __init__(self):

        self.state = "IDLE"

    def set_state(self, state):

        self.state = state

        logger.info(
            f"System state changed to: {state}"
        )

    def get_state(self):

        logger.info(
            f"System state requested: {self.state}"
        )

        return self.state

    def show_state(self):

        print("\nCurrent State:")

        print(self.state)