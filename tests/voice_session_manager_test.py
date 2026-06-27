from brain.voice_session_manager import VoiceSessionManager


session = VoiceSessionManager()

session.start_session(
    "Vinay"
)

session.record_command(
    "Jarvis, start diagnostics"
)

session.show_session()

session.end_session()

session.show_session()