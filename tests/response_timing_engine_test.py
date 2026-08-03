from brain.response_timing_engine import ResponseTimingEngine

ResponseTimingEngine.show_decision(
    voice_activity="SPEAKING",
    silence_duration=0.2
)

ResponseTimingEngine.show_decision(
    voice_activity="POSSIBLE_SPEECH",
    silence_duration=0.8
)

ResponseTimingEngine.show_decision(
    voice_activity="SILENCE",
    silence_duration=2.0
)

ResponseTimingEngine.show_decision(
    voice_activity="SILENCE",
    silence_duration=2.0,
    interruption_detected=True
)