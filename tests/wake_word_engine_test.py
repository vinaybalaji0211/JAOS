from brain.wake_word_engine import WakeWordEngine

engine = WakeWordEngine()

engine.show_status()

print(
    "Detected:",
    engine.detect("Hey Jarvis, start diagnostics")
)

print(
    "Detected:",
    engine.detect("Start diagnostics")
)

engine.set_wake_word("Friday")

print(
    "Detected:",
    engine.detect("Hello Friday")
)