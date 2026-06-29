"""
JAOS Browser Interface

Phase 4 — JAOS-M-0032

Defines the interface that browser providers must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from executive_brain.tools.browser.browser_models import (
    BrowserRequest,
    BrowserResponse,
    BrowserStatus,
)


class BrowserInterface(ABC):
    """
    Base interface for browser providers.
    """

    @property
    @abstractmethod
    def browser_name(self) -> str:
        """
        Returns the browser provider name.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, request: BrowserRequest) -> BrowserResponse:
        """
        Executes a browser action.
        """
        raise NotImplementedError

    @abstractmethod
    def health(self) -> BrowserStatus:
        """
        Returns browser provider availability.
        """
        raise NotImplementedError