from brain.learning_manager import (
    LearningManager
)


manager = LearningManager()

manager.learn(
    "successes",
    "YOLO validation completed"
)

manager.learn(
    "failures",
    "GPU memory exceeded"
)

manager.learn(
    "lessons",
    "Use batch size 4"
)

manager.learn(
    "strategies",
    "Gemini for reasoning"
)

manager.learn(
    "resource_problems",
    "RTX3050 limited VRAM"
)

manager.show_learning()