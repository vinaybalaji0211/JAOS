"""Provider capability validation for intelligence prompt composition."""

from __future__ import annotations

from dataclasses import dataclass

from jaos.ai.provider.provider_config import (
    AIProviderCapability,
    AIProviderConfig,
)


@dataclass(frozen=True, slots=True)
class PromptProviderCapabilityResult:
    """Describes provider compatibility with prompt requirements."""

    required_capabilities: tuple[AIProviderCapability, ...]
    provider_name: str | None
    provider_enabled: bool | None
    supported_capabilities: tuple[AIProviderCapability, ...]
    missing_capabilities: tuple[AIProviderCapability, ...]
    validation_performed: bool
    compatible: bool | None

    def __post_init__(self) -> None:
        if not isinstance(self.required_capabilities, tuple):
            raise TypeError("required_capabilities must be a tuple")

        if not self.required_capabilities:
            raise ValueError("required_capabilities must not be empty")

        for capability in self.required_capabilities:
            if not isinstance(capability, AIProviderCapability):
                raise TypeError(
                    "every required capability must be an "
                    "AIProviderCapability"
                )

        if self.provider_name is not None:
            if not isinstance(self.provider_name, str):
                raise TypeError("provider_name must be a string or None")

            provider_name = self.provider_name.strip().lower()

            if not provider_name:
                raise ValueError(
                    "provider_name must not be empty when provided"
                )

            object.__setattr__(self, "provider_name", provider_name)

        if (
            self.provider_enabled is not None
            and not isinstance(self.provider_enabled, bool)
        ):
            raise TypeError("provider_enabled must be a boolean or None")

        for field_name, capabilities in (
            ("supported_capabilities", self.supported_capabilities),
            ("missing_capabilities", self.missing_capabilities),
        ):
            if not isinstance(capabilities, tuple):
                raise TypeError(f"{field_name} must be a tuple")

            for capability in capabilities:
                if not isinstance(capability, AIProviderCapability):
                    raise TypeError(
                        f"every item in {field_name} must be an "
                        "AIProviderCapability"
                    )

        if not isinstance(self.validation_performed, bool):
            raise TypeError("validation_performed must be a boolean")

        if self.compatible is not None and not isinstance(
            self.compatible,
            bool,
        ):
            raise TypeError("compatible must be a boolean or None")

        if not self.validation_performed:
            if self.provider_name is not None:
                raise ValueError(
                    "provider_name must be None when validation was not "
                    "performed"
                )

            if self.provider_enabled is not None:
                raise ValueError(
                    "provider_enabled must be None when validation was not "
                    "performed"
                )

            if self.supported_capabilities:
                raise ValueError(
                    "supported_capabilities must be empty when validation "
                    "was not performed"
                )

            if self.missing_capabilities:
                raise ValueError(
                    "missing_capabilities must be empty when validation "
                    "was not performed"
                )

            if self.compatible is not None:
                raise ValueError(
                    "compatible must be None when validation was not "
                    "performed"
                )
        else:
            if self.provider_name is None:
                raise ValueError(
                    "provider_name is required when validation was performed"
                )

            if self.provider_enabled is None:
                raise ValueError(
                    "provider_enabled is required when validation was "
                    "performed"
                )

            if self.compatible is None:
                raise ValueError(
                    "compatible is required when validation was performed"
                )

    def to_dict(self) -> dict[str, object]:
        """Return a serialization-friendly validation result."""

        return {
            "required_capabilities": [
                capability.value
                for capability in self.required_capabilities
            ],
            "provider_name": self.provider_name,
            "provider_enabled": self.provider_enabled,
            "supported_capabilities": [
                capability.value
                for capability in self.supported_capabilities
            ],
            "missing_capabilities": [
                capability.value
                for capability in self.missing_capabilities
            ],
            "validation_performed": self.validation_performed,
            "compatible": self.compatible,
        }


class PromptProviderCapabilityValidator:
    """
    Validates prompt requirements against provider configuration metadata.

    This component never initializes, selects, or invokes an AI provider.
    """

    def validate(
        self,
        required_capabilities: tuple[AIProviderCapability, ...],
        provider_config: AIProviderConfig | None = None,
    ) -> PromptProviderCapabilityResult:
        """Return compatibility details for the supplied provider config."""

        normalized_requirements = self._normalize_requirements(
            required_capabilities
        )

        if provider_config is None:
            return PromptProviderCapabilityResult(
                required_capabilities=normalized_requirements,
                provider_name=None,
                provider_enabled=None,
                supported_capabilities=(),
                missing_capabilities=(),
                validation_performed=False,
                compatible=None,
            )

        if not isinstance(provider_config, AIProviderConfig):
            raise TypeError(
                "provider_config must be an AIProviderConfig or None"
            )

        supported = tuple(
            capability
            for capability in normalized_requirements
            if provider_config.supports(capability)
        )
        missing = tuple(
            capability
            for capability in normalized_requirements
            if capability not in supported
        )

        compatible = provider_config.enabled and not missing

        return PromptProviderCapabilityResult(
            required_capabilities=normalized_requirements,
            provider_name=provider_config.name,
            provider_enabled=provider_config.enabled,
            supported_capabilities=supported,
            missing_capabilities=missing,
            validation_performed=True,
            compatible=compatible,
        )

    @staticmethod
    def _normalize_requirements(
        required_capabilities: tuple[AIProviderCapability, ...],
    ) -> tuple[AIProviderCapability, ...]:
        if not isinstance(required_capabilities, tuple):
            raise TypeError("required_capabilities must be a tuple")

        if not required_capabilities:
            raise ValueError("required_capabilities must not be empty")

        normalized: list[AIProviderCapability] = []

        for capability in required_capabilities:
            if not isinstance(capability, AIProviderCapability):
                raise TypeError(
                    "every required capability must be an "
                    "AIProviderCapability"
                )

            if capability not in normalized:
                normalized.append(capability)

        return tuple(normalized)