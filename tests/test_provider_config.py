import pytest

from jaos.ai.provider import (
    AIProviderConfig,
    AIProviderConfigError,
    AIProviderType,
)


def test_provider_config_normalizes_name():
    config = AIProviderConfig(name="  OpenAI  ")

    assert config.name == "openai"


def test_provider_config_rejects_empty_name():
    with pytest.raises(AIProviderConfigError):
        AIProviderConfig(name="   ")


def test_provider_config_defaults_are_safe():
    config = AIProviderConfig(name="mock")

    assert config.provider_type == AIProviderType.CUSTOM
    assert config.enabled is True
    assert config.default_model is None
    assert config.timeout_seconds == 30.0
    assert config.max_retries == 2
    assert config.environment == "default"
    assert config.secret_refs == ()
    assert config.metadata == {}


def test_provider_config_accepts_default_model():
    config = AIProviderConfig(name="ollama", default_model=" llama3 ")

    assert config.default_model == "llama3"


def test_provider_config_empty_default_model_becomes_none():
    config = AIProviderConfig(name="ollama", default_model="   ")

    assert config.default_model is None


def test_provider_config_rejects_invalid_timeout():
    with pytest.raises(AIProviderConfigError):
        AIProviderConfig(name="mock", timeout_seconds=0)


def test_provider_config_rejects_negative_retries():
    with pytest.raises(AIProviderConfigError):
        AIProviderConfig(name="mock", max_retries=-1)


def test_provider_config_normalizes_environment():
    config = AIProviderConfig(name="mock", environment="  Dev  ")

    assert config.environment == "dev"


def test_provider_config_rejects_empty_environment():
    with pytest.raises(AIProviderConfigError):
        AIProviderConfig(name="mock", environment="   ")


def test_provider_config_normalizes_secret_refs():
    config = AIProviderConfig(
        name="openai",
        provider_type=AIProviderType.CLOUD,
        secret_refs=("  OPENAI_API_KEY  ",),
    )

    assert config.secret_refs == ("openai_api_key",)
    assert config.requires_secrets() is True


def test_provider_config_rejects_empty_secret_ref():
    with pytest.raises(AIProviderConfigError):
        AIProviderConfig(name="openai", secret_refs=("   ",))


def test_provider_config_type_helpers():
    local_config = AIProviderConfig(name="ollama", provider_type=AIProviderType.LOCAL)
    cloud_config = AIProviderConfig(name="openai", provider_type=AIProviderType.CLOUD)

    assert local_config.is_local() is True
    assert local_config.is_cloud() is False

    assert cloud_config.is_cloud() is True
    assert cloud_config.is_local() is False


def test_provider_config_metadata_is_copied():
    metadata = {"host": "localhost"}
    config = AIProviderConfig(name="ollama", metadata=metadata)

    metadata["host"] = "changed"

    assert config.metadata["host"] == "localhost"