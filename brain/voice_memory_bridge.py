from logs.logger import logger


class VoiceMemoryBridge:

    def __init__(self):

        self.voice_memories = []

    def store_voice_memory(
            self,
            spoken_text,
            importance="LOW"):

        if importance == "LOW":

            logger.info(
                "Low importance speech ignored."
            )

            return

        memory = {
            "spoken_text": spoken_text,
            "importance": importance
        }

        self.voice_memories.append(
            memory
        )

        logger.info(
            "Voice memory stored."
        )

    def show_memories(self):

        print("\nVoice Memory Bridge:\n")

        if not self.voice_memories:

            print(
                "No voice memories."
            )

            return

        for index, memory in enumerate(
                self.voice_memories,
                start=1):

            print(
                f"{index}. "
                f"{memory['spoken_text']} | "
                f"{memory['importance']}"
            )