"""
JAOS Memory Platform

Provider Capabilities Model

Represents the immutable set of capabilities advertised by a
memory provider.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field

from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)


@dataclass(frozen=True, slots=True)
class ProviderCapabilities:
    """
    Immutable collection of capabilities supported by a provider.
    """

    values: frozenset[ProviderCapability] = field(
        default_factory=frozenset
    )

    def __post_init__(self) -> None:
        """
        Validate and normalize the capability collection.
        """
        normalized = self._normalize(self.values)

        object.__setattr__(self, "values", normalized)

    @classmethod
    def from_iterable(
        cls,
        capabilities: Iterable[ProviderCapability],
    ) -> ProviderCapabilities:
        """
        Create a capability collection from an iterable.
        """
        if isinstance(capabilities, str):
            raise TypeError(
                "capabilities must be an iterable of "
                "ProviderCapability values"
            )

        try:
            normalized = frozenset(capabilities)
        except TypeError as exc:
            raise TypeError(
                "capabilities must be an iterable of "
                "ProviderCapability values"
            ) from exc

        return cls(values=normalized)

    @classmethod
    def empty(cls) -> ProviderCapabilities:
        """
        Return an empty capability collection.
        """
        return cls()

    def supports(
        self,
        capability: ProviderCapability,
    ) -> bool:
        """
        Return whether the provider supports one capability.
        """
        self._validate_capability(capability)

        return capability in self.values

    def supports_all(
        self,
        capabilities: Iterable[ProviderCapability],
    ) -> bool:
        """
        Return whether all requested capabilities are supported.
        """
        requested = self._normalize(capabilities)

        return requested.issubset(self.values)

    def supports_any(
        self,
        capabilities: Iterable[ProviderCapability],
    ) -> bool:
        """
        Return whether at least one requested capability is supported.
        """
        requested = self._normalize(capabilities)

        return bool(self.values.intersection(requested))

    def missing(
        self,
        capabilities: Iterable[ProviderCapability],
    ) -> frozenset[ProviderCapability]:
        """
        Return requested capabilities that are not supported.
        """
        requested = self._normalize(capabilities)

        return requested.difference(self.values)

    def require(
        self,
        capability: ProviderCapability,
    ) -> None:
        """
        Raise an error when a required capability is unavailable.
        """
        self._validate_capability(capability)

        if capability not in self.values:
            raise RuntimeError(
                "Memory provider does not support capability: "
                f"{capability.value}"
            )

    def require_all(
        self,
        capabilities: Iterable[ProviderCapability],
    ) -> None:
        """
        Raise an error when any required capability is unavailable.
        """
        missing = self.missing(capabilities)

        if not missing:
            return

        missing_names = ", ".join(
            sorted(capability.value for capability in missing)
        )

        raise RuntimeError(
            "Memory provider does not support required capabilities: "
            f"{missing_names}"
        )

    def to_sorted_tuple(self) -> tuple[ProviderCapability, ...]:
        """
        Return capabilities in deterministic value order.
        """
        return tuple(
            sorted(
                self.values,
                key=lambda capability: capability.value,
            )
        )

    def __contains__(
        self,
        capability: object,
    ) -> bool:
        """
        Support membership checks.
        """
        return capability in self.values

    def __iter__(self) -> Iterator[ProviderCapability]:
        """
        Iterate over capabilities in deterministic order.
        """
        return iter(self.to_sorted_tuple())

    def __len__(self) -> int:
        """
        Return the number of supported capabilities.
        """
        return len(self.values)

    def __bool__(self) -> bool:
        """
        Return whether any capability is present.
        """
        return bool(self.values)

    @staticmethod
    def _normalize(
        capabilities: Iterable[ProviderCapability],
    ) -> frozenset[ProviderCapability]:
        """
        Validate and normalize an iterable of capabilities.
        """
        if isinstance(capabilities, str):
            raise TypeError(
                "capabilities must contain ProviderCapability values"
            )

        try:
            normalized = frozenset(capabilities)
        except TypeError as exc:
            raise TypeError(
                "capabilities must be an iterable of "
                "ProviderCapability values"
            ) from exc

        for capability in normalized:
            ProviderCapabilities._validate_capability(capability)

        return normalized

    @staticmethod
    def _validate_capability(
        capability: ProviderCapability,
    ) -> None:
        """
        Validate one provider capability.
        """
        if not isinstance(capability, ProviderCapability):
            raise TypeError(
                "capability must be a ProviderCapability"
            )