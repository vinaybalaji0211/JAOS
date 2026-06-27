from brain.emotion_model import (
    EmotionModel
)

emotion = EmotionModel()

emotion.show_state()

emotion.set_state(
    "FOCUSED"
)

emotion.show_state()

emotion.set_state(
    "CURIOUS"
)

emotion.show_state()

emotion.set_state(
    "CONFIDENT"
)

emotion.show_state()