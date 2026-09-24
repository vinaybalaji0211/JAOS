"""
JAOS Browser Manager

Phase 4 — JAOS-M-0032

Manages browser providers.
"""

from __future__ import annotations

from executive_brain.tools.browser.browser_interface import BrowserInterface
from executive_brain.tools.browser.browser_models import (
    BrowserRequest,
    BrowserResponse,
)


class BrowserManager:
    """
    Registers and manages browser providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, BrowserInterface] = {}

    def register_provider(self, provider: BrowserInterface) -> None:
        self._providers[provider.browser_name] = provider

    def unregister_provider(self, browser_name: str) -> None:
        self._providers.pop(browser_name, None)

    def has_provider(self, browser_name: str) -> bool:
        return browser_name in self._providers

    def get_provider(self, browser_name: str) -> BrowserInterface:
        try:
            return self._providers[browser_name]
        except KeyError as error:
            raise KeyError(
                f"Browser provider '{browser_name}' is not registered."
            ) from error

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def execute(
        self,
        browser_name: str,
        request: BrowserRequest,
    ) -> BrowserResponse:
        if not isinstance(request, BrowserRequest):
            raise TypeError("request must be a BrowserRequest")

        provider = self.get_provider(browser_name)

        return provider.execute(request)