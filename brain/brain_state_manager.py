from logs.logger import logger


class BrainStateManager:

    VALID_STATES = [

        "IDLE",

        "UNDERSTANDING",

        "PLANNING",

        "REASONING",

        "EXECUTING",

        "WAITING",

        "ERROR"

    ]

    def __init__(self):

        self.current_state = "IDLE"

    def set_state(self, state):

        state = state.upper()

        if state not in self.VALID_STATES:

            logger.warning(
                f"Invalid brain state: {state}"
            )

            return

        self.current_state = state

        logger.info(
            f"Brain state changed to {state}"
        )

    def get_state(self):

        return self.current_state

    def show_state(self):

        print("\nBrain State:")

        print(self.current_state)