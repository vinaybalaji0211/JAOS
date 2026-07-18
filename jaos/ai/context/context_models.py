from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ContextType(str, Enum):
    CONVERSATION = "conversation"
    MEMORY = "memory"
    IDENTITY = "identity"
    ENVIRONMENT = "environment"
    TASK = "task"
    USER = "user"
    SYSTEM = "system"


@dataclass(frozen=True)
class ContextAssemblyRequest:
    context_types: tuple[ContextType, ...] = ()
    sources: tuple[str, ...] = ()
    max_items: int | None = None
    include_conversation: bool = True

    def __post_init__(self) -> None:
        normalized_sources = tuple(
            source.strip().lower()
            for source in self.sources
            if source.strip()
        )

        if self.max_items is not None and self.max_items <= 0:
            raise ValueError("Context assembly max_items must be greater than zero")

        object.__setattr__(self, "context_types", tuple(self.context_types))
        object.__setattr__(self, "sources", normalized_sources)


@dataclass(frozen=True)
class ContextItem:
    context_type: ContextType
    content: str
    priority: int = 100
    source: str = "manual"
    item_id: str = field(default_factory=lambda: uuid4().hex)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        content = self.content.strip()
        source = self.source.strip().lower()
        item_id = self.item_id.strip()

        if not content:
            raise ValueError("Context item content cannot be empty")

        if not source:
            raise ValueError("Context item source cannot be empty")

        if not item_id:
            raise ValueError("Context item ID cannot be empty")

        object.__setattr__(self, "content", content)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "item_id", item_id)
        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class ConversationTurn:
    role: str
    content: str
    source: str = "conversation"
    turn_id: str = field(default_factory=lambda: uuid4().hex)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        role = self.role.strip().lower()
        content = self.content.strip()
        source = self.source.strip().lower()
        turn_id = self.turn_id.strip()

        if not role:
            raise ValueError("Conversation role cannot be empty")

        if not content:
            raise ValueError("Conversation content cannot be empty")

        if not source:
            raise ValueError("Conversation source cannot be empty")

        if not turn_id:
            raise ValueError("Conversation turn ID cannot be empty")

        object.__setattr__(self, "role", role)
        object.__setattr__(self, "content", content)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "turn_id", turn_id)
        object.__setattr__(self, "metadata", dict(self.metadata or {}))