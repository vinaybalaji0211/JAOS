from jaos.ai.intelligence.provider_profile_models import (
    ProviderCostType,
    ProviderPrivacyType,
    ProviderProfile,
)


class ProviderProfileNotFoundError(Exception):
    """
    Raised when a provider profile cannot be found.
    """


class ProviderProfileRegistry:
    """
    Stores public knowledge about AI providers.

    This registry helps JAOS understand what each provider is useful for.
    It does not store API keys or secrets.
    """

    def __init__(self) -> None:
        self._profiles: dict[str, ProviderProfile] = {}

    def register(self, profile: ProviderProfile) -> None:
        normalized_name = self._normalize_name(profile.name)

        self._profiles[normalized_name] = ProviderProfile(
            name=normalized_name,
            display_name=profile.display_name.strip(),
            description=profile.description.strip(),
            cost_type=profile.cost_type,
            privacy_type=profile.privacy_type,
            strengths=tuple(profile.strengths),
            limitations=tuple(profile.limitations),
            recommended_for=tuple(profile.recommended_for),
        )

    def get(self, name: str) -> ProviderProfile:
        normalized_name = self._normalize_name(name)

        if normalized_name not in self._profiles:
            raise ProviderProfileNotFoundError(
                f"Provider profile not found: {normalized_name}"
            )

        return self._profiles[normalized_name]

    def has(self, name: str) -> bool:
        return self._normalize_name(name) in self._profiles

    def list_profiles(self) -> tuple[ProviderProfile, ...]:
        return tuple(
            self._profiles[name]
            for name in sorted(self._profiles)
        )

    def list_provider_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))

    def count(self) -> int:
        return len(self._profiles)

    def clear(self) -> None:
        self._profiles.clear()

    @staticmethod
    def build_default() -> "ProviderProfileRegistry":
        registry = ProviderProfileRegistry()

        registry.register(
            ProviderProfile(
                name="mock",
                display_name="Mock Provider",
                description="Deterministic test provider for offline development.",
                cost_type=ProviderCostType.FREE,
                privacy_type=ProviderPrivacyType.LOCAL_PRIVATE,
                strengths=(
                    "Testing",
                    "Offline development",
                    "Deterministic responses",
                ),
                limitations=(
                    "Does not provide real reasoning",
                    "Echoes prompt-like responses",
                ),
                recommended_for=(
                    "tests",
                    "offline_development",
                    "platform_validation",
                ),
            )
        )

        registry.register(
            ProviderProfile(
                name="ollama",
                display_name="Ollama",
                description="Local AI runtime for running models on the user's machine.",
                cost_type=ProviderCostType.FREE,
                privacy_type=ProviderPrivacyType.LOCAL_PRIVATE,
                strengths=(
                    "Offline usage",
                    "Privacy",
                    "No API cost",
                    "Local experimentation",
                ),
                limitations=(
                    "Depends on local hardware",
                    "May be slower on low-resource machines",
                    "Model quality depends on installed model",
                ),
                recommended_for=(
                    "offline_tasks",
                    "private_tasks",
                    "low_cost_tasks",
                    "local_development",
                ),
            )
        )

        registry.register(
            ProviderProfile(
                name="openai",
                display_name="OpenAI",
                description="Cloud AI provider suitable for high-quality reasoning and coding.",
                cost_type=ProviderCostType.PAID,
                privacy_type=ProviderPrivacyType.CLOUD,
                strengths=(
                    "Reasoning",
                    "Coding",
                    "Tool use",
                    "General intelligence",
                ),
                limitations=(
                    "Requires internet",
                    "Requires API key",
                    "May incur cost",
                ),
                recommended_for=(
                    "coding",
                    "reasoning",
                    "planning",
                    "complex_tasks",
                ),
            )
        )

        registry.register(
            ProviderProfile(
                name="gemini",
                display_name="Gemini",
                description="Google AI provider with strong multimodal ecosystem potential.",
                cost_type=ProviderCostType.FREE_AND_PAID,
                privacy_type=ProviderPrivacyType.CLOUD,
                strengths=(
                    "Multimodal tasks",
                    "Google ecosystem",
                    "Large context options",
                ),
                limitations=(
                    "Requires internet",
                    "Requires provider configuration",
                    "Cost and limits depend on model tier",
                ),
                recommended_for=(
                    "vision",
                    "multimodal",
                    "google_ecosystem",
                    "large_context",
                ),
            )
        )

        registry.register(
            ProviderProfile(
                name="claude",
                display_name="Claude",
                description="Anthropic AI provider known for long-context reasoning and documents.",
                cost_type=ProviderCostType.PAID,
                privacy_type=ProviderPrivacyType.CLOUD,
                strengths=(
                    "Long-context reasoning",
                    "Document analysis",
                    "Careful writing",
                    "Planning",
                ),
                limitations=(
                    "Requires internet",
                    "Requires API key",
                    "May incur cost",
                ),
                recommended_for=(
                    "documents",
                    "long_context",
                    "planning",
                    "analysis",
                ),
            )
        )

        return registry

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized_name = name.strip().lower()

        if not normalized_name:
            raise ValueError("Provider profile name cannot be empty")

        return normalized_name