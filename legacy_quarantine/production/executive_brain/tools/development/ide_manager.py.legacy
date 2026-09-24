"""
JAOS IDE Manager

Phase 4 — JAOS-M-0033

Manages development environment providers.
"""

from __future__ import annotations

from executive_brain.tools.development.ide_interface import IDEInterface
from executive_brain.tools.development.ide_models import (
    IDERequest,
    IDEResponse,
)


class IDEManager:
    """
    Registers and manages IDE providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, IDEInterface] = {}

    def register_provider(self, provider: IDEInterface) -> None:
        self._providers[provider.ide_name] = provider

    def unregister_provider(self, ide_name: str) -> None:
        self._providers.pop(ide_name, None)

    def has_provider(self, ide_name: str) -> bool:
        return ide_name in self._providers

    def get_provider(self, ide_name: str) -> IDEInterface:
        try:
            return self._providers[ide_name]
        except KeyError as error:
            raise KeyError(
                f"IDE provider '{ide_name}' is not registered."
            ) from error

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def execute(
        self,
        ide_name: str,
        request: IDERequest,
    ) -> IDEResponse:
        if not isinstance(request, IDERequest):
            raise TypeError("request must be an IDERequest")

        provider = self.get_provider(ide_name)

        return provider.execute(request)