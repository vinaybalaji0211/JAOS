from brain.voice_core import VoiceCore


voice = VoiceCore()

voice.enable_voice()

voice.activate_microphone()

voice.activate_speaker()

voice.set_session_state(
    "LISTENING"
)

voice.show_status()