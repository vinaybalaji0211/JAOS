from logs.logger import logger


class NoiseFilter:

    @staticmethod
    def analyze(
            noise_level):

        if noise_level >= 80:
            result = "VERY_NOISY"

        elif noise_level >= 50:
            result = "NOISY"

        elif noise_level >= 20:
            result = "MODERATE"

        else:
            result = "CLEAN"

        logger.info(
            f"Noise analysis: {result}"
        )

        return result

    @staticmethod
    def show_analysis(
            noise_level):

        result = NoiseFilter.analyze(
            noise_level
        )

        print("\nNoise Filter:\n")
        print(f"Noise Level: {noise_level}")
        print(f"Result: {result}")