from logs.logger import logger


class VoiceSessionManager:

    def __init__(self):
        self.session_active = False
        self.session_state = "IDLE"
        self.active_speaker = None
        self.last_command = None

    def start_session(self, speaker="Unknown"):
        self.session_active = True
        self.session_state = "ACTIVE"
        self.active_speaker = speaker

        logger.info("Voice session started.")

    def end_session(self):
        self.session_active = False
        self.session_state = "ENDED"

        logger.info("Voice session ended.")

    def record_command(self, command):
        self.last_command = command

        logger.info("Voice command recorded.")

    def show_session(self):
        print("\nVoice Session Manager:\n")
        print(f"Session Active: {self.session_active}")
        print(f"Session State: {self.session_state}")
        print(f"Active Speaker: {self.active_speaker}")
        print(f"Last Command: {self.last_command}")