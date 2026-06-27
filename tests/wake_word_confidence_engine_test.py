from brain.wake_word_confidence_engine import (
    WakeWordConfidenceEngine
)

WakeWordConfidenceEngine.show_confidence(
    detected=True,
    signal_quality=30,
    noise_level=5
)

WakeWordConfidenceEngine.show_confidence(
    detected=True,
    signal_quality=10,
    noise_level=40
)