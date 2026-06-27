from brain.reflection_engine import (
    ReflectionEngine
)


engine = ReflectionEngine()

engine.reflect(
    "Plugin installation",
    "SUCCESS",
    "Trust score validation works."
)

engine.reflect(
    "Security attack",
    "FAILURE",
    "Need stronger threat monitoring."
)

engine.show_reflections()