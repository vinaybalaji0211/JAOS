from logs.logger import logger


class SpeakerIdentification:

    def __init__(self):

        self.speakers = {}

    def register_speaker(
            self,
            name,
            role):

        self.speakers[name.lower()] = role

        logger.info(
            f"Speaker registered: {name}"
        )

    def identify(
            self,
            speaker_name):

        speaker_name = speaker_name.lower()

        if speaker_name in self.speakers:

            return {
                "name": speaker_name,
                "role": self.speakers[
                    speaker_name
                ]
            }

        return {
            "name": speaker_name,
            "role": "UNKNOWN"
        }

    def show_identification(
            self,
            speaker_name):

        result = self.identify(
            speaker_name
        )

        print(
            "\nSpeaker Identification:\n"
        )

        print(
            f"Speaker: "
            f"{result['name']}"
        )

        print(
            f"Role: "
            f"{result['role']}"
        )