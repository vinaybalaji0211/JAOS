from logs.logger import logger


class WakeWordEngine:

    def __init__(self, wake_word="jarvis"):
        self.wake_word = wake_word.lower()
        self.enabled = True

    def set_wake_word(self, wake_word):
        self.wake_word = wake_word.lower()
        logger.info(f"Wake word changed to {wake_word}")

    def detect(self, speech_text):
        if not self.enabled:
            return False

        return self.wake_word in speech_text.lower()

    def show_status(self):
        print("\nWake Word Engine:\n")
        print(f"Enabled: {self.enabled}")
        print(f"Wake Word: {self.wake_word}")