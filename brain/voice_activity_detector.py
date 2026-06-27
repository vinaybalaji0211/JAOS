from logs.logger import logger


class VoiceActivityDetector:

    @staticmethod
    def detect(audio_level):

        if audio_level >= 50:
            state = "SPEAKING"

        elif audio_level >= 10:
            state = "POSSIBLE_SPEECH"

        else:
            state = "SILENCE"

        logger.info(
            f"Voice activity: {state}"
        )

        return state

    @staticmethod
    def show_state(audio_level):

        state = (
            VoiceActivityDetector.detect(
                audio_level
            )
        )

        print(
            "\nVoice Activity Detector:\n"
        )

        print(
            f"Audio Level: "
            f"{audio_level}"
        )

        print(
            f"State: "
            f"{state}"
        )