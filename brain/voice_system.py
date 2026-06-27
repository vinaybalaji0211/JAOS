from logs.logger import logger


class VoiceSystem:

    def __init__(self):

        self.wake_word = "jarvis"

        self.voice_enabled = True

        self.voice_identity = "male"

        self.speech_rate = 1.0

    def set_voice_identity(
            self,
            identity):

        self.voice_identity = identity

        logger.info(
            f"Voice identity changed to {identity}"
        )

    def set_speech_rate(
            self,
            rate):

        self.speech_rate = rate

        logger.info(
            f"Speech rate changed to {rate}"
        )

    def detect_wake_word(
            self,
            text):

        return self.wake_word.lower() in text.lower()

    def show_status(self):

        print("\nVoice System:\n")

        print(
            f"Wake Word: {self.wake_word}"
        )

        print(
            f"Voice Enabled: {self.voice_enabled}"
        )

        print(
            f"Voice Identity: {self.voice_identity}"
        )

        print(
            f"Speech Rate: {self.speech_rate}"
        )