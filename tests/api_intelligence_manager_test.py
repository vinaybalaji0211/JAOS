from infrastructure.api_intelligence_manager import APIIntelligenceManager

manager = APIIntelligenceManager()

manager.register_api(
    "OpenAI",
    "READY",
    "85%",
    "Cloud"
)

manager.register_api(
    "Gemini",
    "READY",
    "Unlimited",
    "Cloud"
)

manager.register_api(
    "Ollama",
    "READY",
    "Local",
    "Local"
)

manager.show_apis()

print(
    manager.api_status(
        "OpenAI"
    )
)