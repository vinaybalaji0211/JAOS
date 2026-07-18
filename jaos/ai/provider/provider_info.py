from dataclasses import dataclass


@dataclass(frozen=True)
class AIProviderCapabilities:
    supports_text_generation: bool = True
    supports_streaming: bool = False
    supports_tools: bool = False
    supports_vision: bool = False
    supports_audio: bool = False


@dataclass(frozen=True)
class AIProviderInfo:
    name: str
    version: str
    models: tuple[str, ...]
    capabilities: AIProviderCapabilities