from logs.logger import logger


class ResponseTimingEngine:

    @staticmethod
    def decide(
            voice_activity,
            silence_duration,
            interruption_detected=False):

        if interruption_detected or voice_activity == "SPEAKING":
            decision = "WAIT"

        elif voice_activity == "POSSIBLE_SPEECH":
            decision = "WAIT_SHORT"

        elif silence_duration >= 1.5:
            decision = "RESPOND"

        else:
            decision = "WAIT"

        logger.info(
            f"Response timing decision: {decision}"
        )

        return decision

    @staticmethod
    def show_decision(
            voice_activity,
            silence_duration,
            interruption_detected=False):

        decision = ResponseTimingEngine.decide(
            voice_activity,
            silence_duration,
            interruption_detected
        )

        print("\nResponse Timing Engine:\n")
        print(f"Voice Activity: {voice_activity}")
        print(f"Silence Duration: {silence_duration}")
        print(f"Interruption Detected: {interruption_detected}")
        print(f"Decision: {decision}")