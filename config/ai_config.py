"""
JAOS AI Configuration

Phase 3 — JAOS-M-0025.1

Centralized AI provider configuration for Alpha.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OllamaConfig:
    """
    Configuration for local Ollama provider.
    """

    base_url: str = "http://localhost:11434"
    default_model: str = "llama3"
    timeout_seconds: int = 60


@dataclass(slots=True, frozen=True)
class OpenAIConfig:
    """
    Configuration for OpenAI provider.
    """

    default_model: str = "gpt-4.1-mini"
    timeout_seconds: int = 60


@dataclass(slots=True, frozen=True)
class AIConfig:
    """
    Root AI configuration.
    """

    default_provider: str = "ollama"
    ollama: OllamaConfig = OllamaConfig()
    openai: OpenAIConfig = OpenAIConfig()


AI_CONFIG = AIConfig()
