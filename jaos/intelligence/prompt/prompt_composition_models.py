"""Prompt composition contracts for the JAOS Intelligence Platform."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from jaos.ai.prompt import CompiledPrompt, PromptSection
from jaos.ai.provider.provider_config import (
    AIProviderCapability,
    AIProviderConfig,
)
from jaos.intelligence.models import ContextBundle, IntelligenceRequest


@dataclass(frozen=True, slots=True)
class PromptCompositionRequest:
    """
    Describes a provider-neutral prompt composition operation.

    The provider configuration is used only for capability validation.
    Prompt composition must never invoke the provider.
    """

    request: IntelligenceRequest
    context_bundle: ContextBundle
    template_id: str
    template_version: str | None = None
    provider_config: AIProviderConfig | None = None
    output_schema: Mapping[str, Any] | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.request, IntelligenceRequest):
            raise TypeError(
                "request must be an IntelligenceRequest instance"
            )

        if not isinstance(self.context_bundle, ContextBundle):
            raise TypeError(
                "context_bundle must be a ContextBundle instance"
            )

        if not isinstance(self.template_id, str):
            raise TypeError("template_id must be a string")

        template_id = self.template_id.strip()

        if not template_id:
            raise ValueError("template_id must not be empty")

        template_version = self.template_version

        if template_version is not None:
            if not isinstance(template_version, str):
                raise TypeError(
                    "template_version must be a string or None"
                )

            template_version = template_version.strip()

            if not template_version:
                raise ValueError(
                    "template_version must not be empty when provided"
                )

        if (
            self.provider_config is not None
            and not isinstance(self.provider_config, AIProviderConfig)
        ):
            raise TypeError(
                "provider_config must be an AIProviderConfig or None"
            )

        if (
            self.output_schema is not None
            and not isinstance(self.output_schema, Mapping)
        ):
            raise TypeError("output_schema must be a mapping or None")

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

        object.__setattr__(self, "template_id", template_id)
        object.__setattr__(self, "template_version", template_version)

        if self.output_schema is not None:
            object.__setattr__(
                self,
                "output_schema",
                dict(self.output_schema),
            )

        object.__setattr__(self, "metadata", dict(self.metadata))


@dataclass(frozen=True, slots=True)
class PromptCompositionResult:
    """
    Contains the compiled AI prompt and its composition trace.

    Supplemental sections exclude the final user section because the existing
    AI Prompt Platform adds that section while compiling the prompt.
    """

    compiled_prompt: CompiledPrompt
    template_reference: str
    supplemental_sections: tuple[PromptSection, ...]
    context_item_ids: tuple[str, ...]
    estimated_prompt_tokens: int
    required_provider_capabilities: tuple[
        AIProviderCapability,
        ...
    ] = (AIProviderCapability.CHAT,)
    redacted_item_ids: tuple[str, ...] = ()
    contained_item_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.compiled_prompt, CompiledPrompt):
            raise TypeError(
                "compiled_prompt must be a CompiledPrompt instance"
            )

        if not isinstance(self.template_reference, str):
            raise TypeError("template_reference must be a string")

        template_reference = self.template_reference.strip()

        if not template_reference:
            raise ValueError("template_reference must not be empty")

        if not isinstance(self.supplemental_sections, tuple):
            raise TypeError("supplemental_sections must be a tuple")

        for section in self.supplemental_sections:
            if not isinstance(section, PromptSection):
                raise TypeError(
                    "every supplemental section must be a PromptSection"
                )

        expected_section_count = len(self.supplemental_sections) + 1

        if self.compiled_prompt.section_count != expected_section_count:
            raise ValueError(
                "compiled prompt section count does not match the "
                "supplemental sections and final user section"
            )

        if not isinstance(self.context_item_ids, tuple):
            raise TypeError("context_item_ids must be a tuple")

        normalized_context_item_ids = self._normalize_identifiers(
            self.context_item_ids,
            "context_item_ids",
        )

        if (
            isinstance(self.estimated_prompt_tokens, bool)
            or not isinstance(self.estimated_prompt_tokens, int)
        ):
            raise TypeError(
                "estimated_prompt_tokens must be an integer"
            )

        if self.estimated_prompt_tokens <= 0:
            raise ValueError(
                "estimated_prompt_tokens must be greater than zero"
            )

        if not isinstance(
            self.required_provider_capabilities,
            tuple,
        ):
            raise TypeError(
                "required_provider_capabilities must be a tuple"
            )

        if not self.required_provider_capabilities:
            raise ValueError(
                "required_provider_capabilities must not be empty"
            )

        for capability in self.required_provider_capabilities:
            if not isinstance(capability, AIProviderCapability):
                raise TypeError(
                    "every required provider capability must be an "
                    "AIProviderCapability"
                )

        normalized_capabilities = tuple(
            dict.fromkeys(self.required_provider_capabilities)
        )

        normalized_redacted_ids = self._normalize_identifiers(
            self.redacted_item_ids,
            "redacted_item_ids",
        )
        normalized_contained_ids = self._normalize_identifiers(
            self.contained_item_ids,
            "contained_item_ids",
        )

        context_id_set = set(normalized_context_item_ids)

        if not set(normalized_redacted_ids).issubset(context_id_set):
            raise ValueError(
                "redacted_item_ids must reference composed context items"
            )

        if not set(normalized_contained_ids).issubset(context_id_set):
            raise ValueError(
                "contained_item_ids must reference composed context items"
            )

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

        object.__setattr__(
            self,
            "template_reference",
            template_reference,
        )
        object.__setattr__(
            self,
            "context_item_ids",
            normalized_context_item_ids,
        )
        object.__setattr__(
            self,
            "required_provider_capabilities",
            normalized_capabilities,
        )
        object.__setattr__(
            self,
            "redacted_item_ids",
            normalized_redacted_ids,
        )
        object.__setattr__(
            self,
            "contained_item_ids",
            normalized_contained_ids,
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    @staticmethod
    def _normalize_identifiers(
        identifiers: tuple[str, ...],
        field_name: str,
    ) -> tuple[str, ...]:
        if not isinstance(identifiers, tuple):
            raise TypeError(f"{field_name} must be a tuple")

        normalized: list[str] = []

        for identifier in identifiers:
            if not isinstance(identifier, str):
                raise TypeError(
                    f"every item in {field_name} must be a string"
                )

            value = identifier.strip()

            if not value:
                raise ValueError(
                    f"every item in {field_name} must be non-empty"
                )

            normalized.append(value)

        if len(normalized) != len(set(normalized)):
            raise ValueError(f"{field_name} must not contain duplicates")

        return tuple(normalized)