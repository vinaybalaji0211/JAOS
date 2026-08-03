from brain.conversation_manager import ConversationManager
from brain.emotion_model import EmotionModel
from brain.human_memory_layer import HumanMemoryLayer
from brain.personality_profile import PersonalityProfile
from brain.voice_system import VoiceSystem

print("\n=== PHASE 7 INTEGRATION TEST ===\n")

# Conversation
conversation = ConversationManager()

conversation.set_topic(
    "Building JARVIS OS"
)

conversation.set_mode(
    "PLANNING"
)

conversation.set_intent(
    "Continue roadmap"
)

conversation.show_state()

# Personality
personality = PersonalityProfile()

personality.update(
    "proactivity",
    1.0
)

personality.show_profile()

# Emotion
emotion = EmotionModel()

emotion.set_state(
    "FOCUSED"
)

emotion.show_state()

# Voice
voice = VoiceSystem()

voice.show_status()

print(
    "Wake word detected:",
    voice.detect_wake_word(
        "Hello Jarvis"
    )
)

# Human memory
memory = HumanMemoryLayer()

memory.remember(
    "Vinay",
    "projects",
    "JARVIS OS"
)

memory.remember(
    "Vinay",
    "preferences",
    "Step-by-step instructions"
)

memory.show_person(
    "Vinay"
)

print("\n=== PHASE 7 COMPLETE ===")