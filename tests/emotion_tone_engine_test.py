from brain.emotion_tone_engine import (
    EmotionToneEngine
)


EmotionToneEngine.show_tone(
    "system success",
    "LOW"
)

EmotionToneEngine.show_tone(
    "module error detected",
    "MEDIUM"
)

EmotionToneEngine.show_tone(
    "security breach",
    "CRITICAL"
)