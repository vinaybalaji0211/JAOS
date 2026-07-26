"""Prompt composer contract for the JAOS Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)

if TYPE_CHECKING:
    from jaos.intelligence.prompt.prompt_composition_models import (
        PromptCompositionRequest,
        PromptCompositionResult,
    )


class PromptComposer(IntelligenceComponent):
    """Contract for provider-neutral intelligence prompt composition."""

    @abstractmethod
    def compose(
        self,
        composition_request: PromptCompositionRequest,
    ) -> PromptCompositionResult:
        """
        Compose a provider-neutral prompt without invoking a provider.

        Implementations must preserve instruction authority boundaries,
        validate request/context alignment, and return prompt trace metadata.
        """

        raise NotImplementedError