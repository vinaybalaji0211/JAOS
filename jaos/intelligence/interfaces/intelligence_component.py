"""Base component contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import ABC, abstractmethod


class IntelligenceComponent(ABC):
    """
    Defines the lifecycle contract for Intelligence Platform components.

    All intelligence components participate in a common lifecycle while
    remaining responsible for their own internal state. Platform
    composition coordinates initialization, readiness, and shutdown.
    """

    @property
    @abstractmethod
    def component_name(self) -> str:
        """
        Return the stable component name.

        The returned value should uniquely identify the component within
        the JAOS Intelligence Platform.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """
        Return whether the component is ready to accept work.

        This property must perform only an in-memory state check and
        must not perform I/O.
        """

        raise NotImplementedError

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the component and its dependencies.

        Implementations may perform asynchronous initialization such as:

        - Loading configuration
        - Connecting to external services
        - Warming local models
        - Initializing caches
        - Allocating runtime resources
        """

        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        """
        Gracefully release component resources.

        Implementations may perform asynchronous cleanup such as:

        - Closing network sessions
        - Releasing model resources
        - Flushing telemetry
        - Persisting transient state
        - Closing database connections
        """

        raise NotImplementedError
