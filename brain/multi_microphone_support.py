from logs.logger import logger


class MultiMicrophoneSupport:

    def __init__(self):

        self.microphones = []

    def add_microphone(
            self,
            mic_name):

        self.microphones.append(
            mic_name
        )

        logger.info(
            f"Microphone added: {mic_name}"
        )

    def remove_microphone(
            self,
            mic_name):

        if mic_name in self.microphones:

            self.microphones.remove(
                mic_name
            )

            logger.info(
                f"Microphone removed: {mic_name}"
            )

    def show_microphones(self):

        print(
            "\nMulti-Microphone Support:\n"
        )

        if not self.microphones:

            print(
                "No microphones configured."
            )

            return

        for index, mic in enumerate(
                self.microphones,
                start=1):

            print(
                f"{index}. {mic}"
            )