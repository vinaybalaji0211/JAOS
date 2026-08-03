from brain.voice_command_prioritizer import VoiceCommandPrioritizer

prioritizer = VoiceCommandPrioritizer()

prioritizer.add_command(
    "Play music",
    "BACKGROUND"
)

prioritizer.add_command(
    "Emergency lockdown",
    "EMERGENCY"
)

prioritizer.add_command(
    "Run security scan",
    "SECURITY"
)

prioritizer.add_command(
    "Open browser",
    "NORMAL"
)

prioritizer.add_command(
    "Author override",
    "AUTHOR"
)

prioritizer.show_commands()