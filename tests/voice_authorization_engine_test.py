from brain.voice_authorization_engine import (
    VoiceAuthorizationEngine
)

engine = VoiceAuthorizationEngine()

engine.show_authorization(
    "AUTHOR",
    "SECURITY_ACCESS"
)

engine.show_authorization(
    "TRUSTED",
    "NORMAL_COMMANDS"
)

engine.show_authorization(
    "UNKNOWN",
    "SECURITY_ACCESS"
)