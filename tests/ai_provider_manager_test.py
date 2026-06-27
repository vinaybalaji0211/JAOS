from infrastructure.ai_provider_manager import (
    AIProviderManager
)

manager = AIProviderManager()

manager.register_provider(
    "OpenAI",
    "READY"
)

manager.register_provider(
    "Gemini",
    "READY"
)

manager.register_provider(
    "Ollama",
    "OFFLINE"
)

manager.show_providers()

print(
    "\nGemini:",
    manager.provider_status("Gemini")
)