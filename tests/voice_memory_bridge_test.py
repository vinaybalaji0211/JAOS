from brain.voice_memory_bridge import (
    VoiceMemoryBridge
)

bridge = VoiceMemoryBridge()

bridge.store_voice_memory(
    "Remember that security threat response engine is important",
    "HIGH"
)

bridge.store_voice_memory(
    "background noise text",
    "LOW"
)

bridge.store_voice_memory(
    "User prefers strong and secure JARVIS",
    "HIGH"
)

bridge.show_memories()