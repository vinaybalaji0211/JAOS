from logs.logger import logger


class EmotionToneEngine:

    @staticmethod
    def choose_tone(
            situation,
            risk_level="LOW"):

        situation = situation.lower()

        if risk_level == "CRITICAL":
            tone = "EMERGENCY"

        elif risk_level == "HIGH":
            tone = "URGENT"

        elif "error" in situation:
            tone = "CAUTIOUS"

        elif "learning" in situation:
            tone = "FOCUSED"

        elif "success" in situation:
            tone = "CONFIDENT"

        else:
            tone = "CALM"

        logger.info(
            f"Tone selected: {tone}"
        )

        return tone

    @staticmethod
    def show_tone(
            situation,
            risk_level="LOW"):

        tone = EmotionToneEngine.choose_tone(
            situation,
            risk_level
        )

        print("\nEmotion & Tone Engine:\n")
        print(f"Situation: {situation}")
        print(f"Risk Level: {risk_level}")
        print(f"Tone: {tone}")