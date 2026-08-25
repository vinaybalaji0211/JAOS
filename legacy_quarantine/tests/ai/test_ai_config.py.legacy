from config.ai_config import (
    AI_CONFIG,
    AIConfig,
    OllamaConfig,
    OpenAIConfig,
)


def test_ollama_config_defaults():
    config = OllamaConfig()

    assert config.base_url == "http://localhost:11434"
    assert config.default_model == "llama3"
    assert config.timeout_seconds == 60


def test_openai_config_defaults():
    config = OpenAIConfig()

    assert config.default_model == "gpt-4.1-mini"
    assert config.timeout_seconds == 60


def test_ai_config_defaults():
    config = AIConfig()

    assert config.default_provider == "ollama"
    assert isinstance(config.ollama, OllamaConfig)
    assert isinstance(config.openai, OpenAIConfig)


def test_global_ai_config_instance():
    assert isinstance(AI_CONFIG, AIConfig)
    assert AI_CONFIG.default_provider == "ollama"