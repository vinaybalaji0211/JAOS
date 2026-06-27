from logs.logger import logger


class PersonalityProfile:

    def __init__(self):

        self.profile = {

            "name": "JARVIS",

            "tone": "professional",

            "conversation_style": "natural",

            "humor": 0.2,

            "proactivity": 0.9,

            "curiosity": 0.8,

            "formality": "balanced",

            "voice_identity": "male"

        }

    def update(
            self,
            key,
            value):

        self.profile[key] = value

        logger.info(
            f"Personality updated: {key}"
        )

    def get(
            self,
            key):

        return self.profile.get(
            key
        )

    def show_profile(self):

        print("\nPersonality Profile:\n")

        for key, value in self.profile.items():

            print(
                f"{key}: {value}"
            )