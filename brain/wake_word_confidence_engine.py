from logs.logger import logger


class WakeWordConfidenceEngine:

    @staticmethod
    def evaluate(
            detected,
            signal_quality,
            noise_level):

        confidence = 0

        if detected:
            confidence += 60

        confidence += signal_quality

        confidence -= noise_level

        confidence = max(
            0,
            min(100, confidence)
        )

        logger.info(
            f"Wake-word confidence: {confidence}"
        )

        return confidence

    @staticmethod
    def show_confidence(
            detected,
            signal_quality,
            noise_level):

        confidence = (
            WakeWordConfidenceEngine.evaluate(
                detected,
                signal_quality,
                noise_level
            )
        )

        print(
            "\nWake Word Confidence Engine:\n"
        )

        print(
            f"Confidence: {confidence}%"
        )

        if confidence >= 80:
            print("Decision: ACCEPT")

        elif confidence >= 50:
            print("Decision: REVIEW")

        else:
            print("Decision: REJECT")