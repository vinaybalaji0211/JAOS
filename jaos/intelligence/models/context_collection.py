"""Collection of validated context objects for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from jaos.intelligence.models.context import Context
from jaos.intelligence.models.context_priority import ContextPriority
from jaos.intelligence.models.context_type import ContextType


@dataclass(frozen=True, slots=True)
class ContextCollection:
    """
    Represents the complete contextual information available
    for a reasoning operation.
    """

    contexts: tuple[Context, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate the context collection."""

        if isinstance(self.contexts, Context):
            raise TypeError(
                "contexts must be a collection of Context objects"
            )

        try:
            items = tuple(self.contexts)
        except TypeError as exc:
            raise TypeError(
                "contexts must be iterable"
            ) from exc

        for item in items:
            if not isinstance(item, Context):
                raise TypeError(
                    "contexts must contain only Context objects"
                )

        object.__setattr__(self, "contexts", items)

    @property
    def count(self) -> int:
        """Return the number of contexts."""

        return len(self.contexts)

    def is_empty(self) -> bool:
        """Return True if no contexts exist."""

        return not self.contexts

    def by_type(
        self,
        context_type: ContextType,
    ) -> tuple[Context, ...]:
        """Return all contexts of the requested type."""

        return tuple(
            context
            for context in self.contexts
            if context.context_type is context_type
        )

    def by_priority(
        self,
        priority: ContextPriority,
    ) -> tuple[Context, ...]:
        """Return contexts matching the given priority."""

        return tuple(
            context
            for context in self.contexts
            if context.priority is priority
        )

    def highest_priority(self) -> Context | None:
        """Return the highest-priority context."""

        if not self.contexts:
            return None

        return max(
            self.contexts,
            key=lambda context: context.priority,
        )

    def sorted_by_priority(
        self,
        descending: bool = True,
    ) -> tuple[Context, ...]:
        """Return contexts ordered by priority."""

        return tuple(
            sorted(
                self.contexts,
                key=lambda context: context.priority,
                reverse=descending,
            )
        )

    def to_dict(self) -> dict:
        """Return a provider-independent representation."""

        return {
            "count": self.count,
            "contexts": [
                context.to_dict()
                for context in self.contexts
            ],
        }

    @classmethod
    def from_iterable(
        cls,
        contexts: Iterable[Context],
    ) -> ContextCollection:
        """Construct a collection from any iterable."""

        return cls(tuple(contexts))