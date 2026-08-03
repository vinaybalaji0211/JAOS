from brain.web_learning_engine import WebLearningEngine

engine = (
    WebLearningEngine()
)

engine.learn(
    "Wikipedia",
    "Quantum Physics"
)

engine.learn(
    "MIT OpenCourseWare",
    "Wave Mechanics"
)

engine.learn(
    "Stanford Encyclopedia",
    "Quantum Computing"
)

engine.show_learning()