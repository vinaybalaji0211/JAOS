"""Reasoning engine contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.reasoning_request import (
    ReasoningRequest,
)
from jaos.intelligence.models.reasoning_result import (
    ReasoningResult,
)


class ReasoningEngine(IntelligenceComponent):
    """
    Defines the provider-independent contract for structured reasoning.

    The Reasoning Engine is responsible exclusively for transforming a
    validated ReasoningRequest into a structured ReasoningResult.

    Implementations perform cognitive analysis such as:

    - Objective interpretation
    - Context analysis
    - Assumption generation
    - Constraint identification
    - Ambiguity and gap detection
    - Hypothesis and trade-off evaluation
    - Risk and impact assessment
    - Reasoning result synthesis

    The Reasoning Engine represents a pure cognitive boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Produce structured reasoning results
    - Remain free of observable side effects

    Implementations shall not:

    - Execute tools
    - Generate execution plans
    - Enforce security policies
    - Modify persistent memory
    - Perform provider routing
    - Construct provider-specific prompts
    - Execute external actions
    """

    @abstractmethod
    async def reason(
        self,
        request: ReasoningRequest,
    ) -> ReasoningResult:
        """
        Perform structured reasoning for a validated request.

        The implementation performs one complete cognitive transaction,
        transforming the supplied ReasoningRequest into a structured
        ReasoningResult.

        This operation represents the single public entry point into the
        reasoning process. All subordinate cognitive activities remain
        encapsulated as implementation details.

        Args:
            request:
                The validated reasoning request.

        Returns:
            A structured provider-independent ReasoningResult.

        Raises:
            ReasoningException:
                If structured reasoning cannot be completed.
        """

        raise NotImplementedError
