from brain.embodied_learning_engine import EmbodiedLearningEngine

engine = EmbodiedLearningEngine()

engine.learn(
    "VS Code Workflow",
    "Environment should be activated before tests."
)

engine.learn(
    "YOLO Training",
    "Dataset validation reduces training errors."
)

engine.learn(
    "Research Workflow",
    "Multiple source verification improves accuracy."
)

engine.show_learning()