from logs.logger import logger


class AudioQualityAnalyzer:

    @staticmethod
    def evaluate(
            signal_strength,
            noise_level,
            voice_clarity):

        score = (
            signal_strength +
            voice_clarity -
            noise_level
        )

        score = max(
            0,
            min(100, score)
        )

        logger.info(
            f"Audio quality score: {score}"
        )

        return score

    @staticmethod
    def show_quality(
            signal_strength,
            noise_level,
            voice_clarity):

        score = (
            AudioQualityAnalyzer.evaluate(
                signal_strength,
                noise_level,
                voice_clarity
            )
        )

        print(
            "\nAudio Quality Analyzer:\n"
        )

        print(
            f"Signal Strength: "
            f"{signal_strength}"
        )

        print(
            f"Noise Level: "
            f"{noise_level}"
        )

        print(
            f"Voice Clarity: "
            f"{voice_clarity}"
        )

        print(
            f"Quality Score: "
            f"{score}"
        )