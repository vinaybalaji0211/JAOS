"""Prompt composer contract for the JAOS AI Intelligence Platform."""

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
    """
    Defines the provider-independent contract for prompt composition.

    The Prompt Composer is responsible exclusively for transforming
    structured intelligence artifacts into provider-neutral prompt
    compositions.

    Implementations perform prompt composition activities such as:

    - Instruction hierarchy composition
    - Context integration
    - Prompt normalization
    - Request validation
    - Prompt trace generation
    - Prompt metadata synthesis

    The Prompt Composer represents the prompt construction boundary.

    Implementations shall:

    - Operate asynchronously
    - Remain provider independent
    - Preserve instruction authority
    - Use JAOS prompt composition models exclusively
    - Produce deterministic prompt compositions
    - Remain free of observable side effects

    Implementations shall not:

    - Invoke AI providers
    - Perform provider routing
    - Execute reasoning
    - Generate execution plans
    - Execute tools
    - Execute external actions
    """

    @abstractmethod
    async def compose(
        self,
        composition_request: PromptCompositionRequest,
    ) -> PromptCompositionResult:
        """
        Compose a provider-neutral prompt.

        Implementations transform a validated
        PromptCompositionRequest into a structured
        PromptCompositionResult without invoking an AI provider.

        Args:
            composition_request:
                The prompt composition request.

        Returns:
            A provider-independent PromptCompositionResult.
        """

        raise NotImplementedError
