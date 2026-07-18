from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self


class MemoryTransaction(ABC):
    """
    Contract for transactional memory operations.
    """

    @abstractmethod
    def commit(self) -> None:
        """
        Commit all pending memory operations.
        """

    @abstractmethod
    def rollback(self) -> None:
        """
        Roll back all pending memory operations.
        """

    @abstractmethod
    def __enter__(self) -> Self:
        """
        Enter the transaction context.
        """

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """
        Exit the transaction context.
        """