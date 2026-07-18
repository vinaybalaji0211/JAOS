"""
JAOS Memory Platform

Provider Descriptor

Describes one memory provider and its advertised capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass

from jaos.memory.providers.provider_capabilities import (
    ProviderCapabilities,
)


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    """
    Immutable description of a memory provider.
    """

    provider_id: str

    provider_name: str

    provider_version: str

    capabilities: ProviderCapabilities

    description: str = ""

    author: str = "JAOS"

    supports_persistence: bool = True

    is_default: bool = False

    def __post_init__(self) -> None:
        """
        Validate descriptor fields.
        """
        self._validate_non_empty(
            self.provider_id,
            "provider_id",
        )

        self._validate_non_empty(
            self.provider_name,
            "provider_name",
        )

        self._validate_non_empty(
            self.provider_version,
            "provider_version",
        )

        if not isinstance(
            self.capabilities,
            ProviderCapabilities,
        ):
            raise TypeError(
                "capabilities must be a "
                "ProviderCapabilities instance"
            )

    @property
    def capability_count(self) -> int:
        """
        Return the number of advertised capabilities.
        """
        return len(self.capabilities)

    def supports(self, capability) -> bool:
        """
        Convenience wrapper around ProviderCapabilities.
        """
        return self.capabilities.supports(capability)

    @staticmethod
    def _validate_non_empty(
        value: str,
        field_name: str,
    ) -> None:
        """
        Validate a required string.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string"
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} must not be empty"
            )