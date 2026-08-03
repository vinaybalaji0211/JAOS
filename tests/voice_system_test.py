from brain.voice_system import VoiceSystem

voice = VoiceSystem()

voice.show_status()

print()

print(
    "Wake word detected:",
    voice.detect_wake_word(
        "Hello Jarvis"
    )
)

voice.set_voice_identity(
    "male"
)

voice.set_speech_rate(
    1.1
)

voice.show_status()