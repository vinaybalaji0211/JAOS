from brain.voice_core import VoiceCore
from brain.voice_session_manager import VoiceSessionManager
from brain.wake_word_engine import WakeWordEngine
from brain.wake_word_confidence_engine import WakeWordConfidenceEngine
from brain.conversation_manager import ConversationManager
from brain.interruption_handler import InterruptionHandler
from brain.emotion_tone_engine import EmotionToneEngine
from brain.noise_filter import NoiseFilter
from brain.audio_quality_analyzer import AudioQualityAnalyzer
from brain.voice_activity_detector import VoiceActivityDetector
from brain.response_timing_engine import ResponseTimingEngine
from brain.voice_memory_bridge import VoiceMemoryBridge
from brain.speaker_identification import SpeakerIdentification
from brain.voice_authorization_engine import VoiceAuthorizationEngine
from brain.voice_security_layer import VoiceSecurityLayer
from brain.multi_microphone_support import MultiMicrophoneSupport
from brain.voice_command_prioritizer import VoiceCommandPrioritizer


print("\n=== PHASE 15 INTEGRATION TEST ===\n")

voice = VoiceCore()
voice.enable_voice()
voice.activate_microphone()
voice.activate_speaker()
voice.set_session_state("LISTENING")
voice.show_status()

session = VoiceSessionManager()
session.start_session("Vinay")
session.record_command("Jarvis, run security scan")
session.show_session()

wake = WakeWordEngine()
print("\nWake Word Detected:", wake.detect("Hey Jarvis, run diagnostics"))

WakeWordConfidenceEngine.show_confidence(
    detected=True,
    signal_quality=30,
    noise_level=5
)

conversation = ConversationManager()
conversation.start()
conversation.add_message("User", "Jarvis, run diagnostics.")
conversation.add_message("Jarvis", "Diagnostics started.")
conversation.show_history()

handler = InterruptionHandler()
handler.start_task("Voice response")
handler.interrupt("User command")
handler.show_status()

EmotionToneEngine.show_tone(
    "security breach",
    "CRITICAL"
)

NoiseFilter.show_analysis(30)

AudioQualityAnalyzer.show_quality(
    signal_strength=80,
    noise_level=10,
    voice_clarity=85
)

VoiceActivityDetector.show_state(80)

ResponseTimingEngine.show_decision(
    voice_activity="SILENCE",
    silence_duration=2.0
)

memory = VoiceMemoryBridge()
memory.store_voice_memory(
    "User prefers strong and secure JARVIS",
    "HIGH"
)
memory.show_memories()

speaker = SpeakerIdentification()
speaker.register_speaker("Vinay", "AUTHOR")
speaker.show_identification("Vinay")

auth = VoiceAuthorizationEngine()
auth.show_authorization("AUTHOR", "SECURITY_ACCESS")

security = VoiceSecurityLayer()
security.show_validation("AUTHOR", "SECURITY_ACCESS")

mics = MultiMicrophoneSupport()
mics.add_microphone("Laptop Mic")
mics.add_microphone("USB Mic")
mics.show_microphones()

prioritizer = VoiceCommandPrioritizer()
prioritizer.add_command("Play music", "BACKGROUND")
prioritizer.add_command("Emergency lockdown", "EMERGENCY")
prioritizer.add_command("Run security scan", "SECURITY")
prioritizer.show_commands()

print("\n=== PHASE 15 COMPLETE ===")