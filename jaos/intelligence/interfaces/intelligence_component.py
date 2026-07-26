"""Base component contract for the JAOS AI Intelligence Platform."""

from abc import ABC, abstractmethod


class IntelligenceComponent(ABC):
    """
    Defines the lifecycle contract for intelligence components.

    Implementations control their own internal state while platform
    composition coordinates initialization and shutdown.
    """

    @property
    @abstractmethod
    def component_name(self) -> str:
        """Return the stable component name."""

        raise NotImplementedError

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """Return whether the component can currently accept work."""

        raise NotImplementedError

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the component and its dependencies."""

        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """Release component resources safely."""

        raise NotImplementedError