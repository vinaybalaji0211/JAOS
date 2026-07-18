from typing import Protocol

from jaos.ai.prompt.prompt_models import PromptSection


class PromptContributor(Protocol):
    """
    Interface for components that contribute prompt sections.

    Future platforms such as Memory, Tools, Identity, Vision, and Executive
    can implement this protocol without changing PromptBuilder.
    """

    def contribute(self) -> tuple[PromptSection, ...]:
        """Return prompt sections contributed by this component."""


class StaticPromptContributor:
    """
    Simple contributor for fixed prompt sections.

    Useful for tests, runtime defaults, and lightweight Alpha integrations.
    """

    def __init__(self, sections: tuple[PromptSection, ...]) -> None:
        self._sections = tuple(sections)

    def contribute(self) -> tuple[PromptSection, ...]:
        return self._sections