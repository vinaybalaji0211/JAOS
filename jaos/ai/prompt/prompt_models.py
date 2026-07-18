from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PromptSectionType(str, Enum):
    SYSTEM = "system"
    IDENTITY = "identity"
    CONTEXT = "context"
    MEMORY = "memory"
    TOOLS = "tools"
    USER = "user"
    INSTRUCTION = "instruction"


@dataclass(frozen=True)
class PromptSection:
    section_type: PromptSectionType
    content: str
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        content = self.content.strip()

        if not content:
            raise ValueError("Prompt section content cannot be empty")

        object.__setattr__(self, "content", content)
        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class PromptBuildRequest:
    user_prompt: str
    sections: tuple[PromptSection, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        user_prompt = self.user_prompt.strip()

        if not user_prompt:
            raise ValueError("User prompt cannot be empty")

        object.__setattr__(self, "user_prompt", user_prompt)
        object.__setattr__(self, "sections", tuple(self.sections))
        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class CompiledPrompt:
    """
    Final prompt produced by the Prompt Platform.

    The text is what providers receive.
    Metadata gives JAOS traceability for debugging, diagnostics, and future
    prompt optimization.
    """

    text: str
    section_count: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        text = self.text.strip()

        if not text:
            raise ValueError("Compiled prompt text cannot be empty")

        if self.section_count <= 0:
            raise ValueError("Compiled prompt section_count must be greater than zero")

        object.__setattr__(self, "text", text)
        object.__setattr__(self, "metadata", dict(self.metadata or {}))