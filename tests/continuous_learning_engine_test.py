from brain.continuous_learning_engine import ContinuousLearningEngine

engine = (
    ContinuousLearningEngine()
)

engine.learn(
    "Classical Physics"
)

engine.learn(
    "Wave Mechanics"
)

engine.learn(
    "Quantum States"
)

engine.show_progress()

print(
    engine.has_learned(
        "Wave Mechanics"
    )
)