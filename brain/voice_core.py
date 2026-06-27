from logs.logger import logger


class VoiceCore:

    def __init__(self):

        self.voice_enabled = False
        self.microphone_active = False
        self.speaker_active = False
        self.session_state = "IDLE"

    def enable_voice(self):

        self.voice_enabled = True

        logger.info(
            "Voice enabled."
        )

    def disable_voice(self):

        self.voice_enabled = False

        logger.info(
            "Voice disabled."
        )

    def activate_microphone(self):

        self.microphone_active = True

        logger.info(
            "Microphone activated."
        )

    def activate_speaker(self):

        self.speaker_active = True

        logger.info(
            "Speaker activated."
        )

    def set_session_state(
            self,
            state):

        self.session_state = state

        logger.info(
            f"Voice session state: {state}"
        )

    def show_status(self):

        print("\nVoice Core:\n")

        print(
            f"Voice Enabled: {self.voice_enabled}"
        )

        print(
            f"Microphone Active: "
            f"{self.microphone_active}"
        )

        print(
            f"Speaker Active: "
            f"{self.speaker_active}"
        )

        print(
            f"Session State: "
            f"{self.session_state}"
        )