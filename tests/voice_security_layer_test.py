from brain.voice_security_layer import VoiceSecurityLayer

security = VoiceSecurityLayer()

security.show_validation(
    "AUTHOR",
    "SECURITY_ACCESS"
)

security.show_validation(
    "TRUSTED",
    "SECURITY_ACCESS"
)

security.show_validation(
    "UNKNOWN",
    "NORMAL_COMMAND"
)