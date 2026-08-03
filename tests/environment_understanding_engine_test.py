from brain.environment_understanding_engine import EnvironmentUnderstandingEngine

engine = EnvironmentUnderstandingEngine()

engine.update_environment(
    "Operating System",
    "Windows 11"
)

engine.update_environment(
    "GPU",
    "RTX 3050 Laptop"
)

engine.update_environment(
    "Primary Project",
    "JARVIS"
)

engine.show_environment()