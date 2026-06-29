"""
JAOS IDE Interface

Phase 4 — JAOS-M-0033

Defines the interface for development environment providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from executive_brain.tools.development.ide_models import (
    IDERequest,
    IDEResponse,
    IDEStatus,
)


class IDEInterface(ABC):
    """
    Base interface for IDE providers.
    """

    @property
    @abstractmethod
    def ide_name(self) -> str:
        """
        Returns the IDE provider name.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, request: IDERequest) -> IDEResponse:
        """
        Executes a development action.
        """
        raise NotImplementedError

    @abstractmethod
    def health(self) -> IDEStatus:
        """
        Returns the provider availability.
        """
        raise NotImplementedError