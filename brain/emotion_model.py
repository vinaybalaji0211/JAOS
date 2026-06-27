from logs.logger import logger


class EmotionModel:

    def __init__(self):

        self.state = "NEUTRAL"

    def set_state(
            self,
            state):

        self.state = state

        logger.info(
            f"Emotion state changed to {state}"
        )

    def get_state(self):

        return self.state

    def show_state(self):

        print("\nEmotion Model:\n")

        print(
            f"Current State: {self.state}"
        )