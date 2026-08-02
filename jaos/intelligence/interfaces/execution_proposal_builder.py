"""Execution proposal builder contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.execution_proposal import (
    ExecutionProposal,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)
from jaos.intelligence.models.proposed_plan_step import (
    ProposedPlanStep,
)


class ExecutionProposalBuilder(IntelligenceComponent):
    """
    Defines the provider-independent contract for execution proposal
    construction.

    The Execution Proposal Builder is responsible exclusively for
    transforming planning artifacts into structured execution
    proposals suitable for downstream evaluation and execution.

    Implementations perform execution proposal activities such as:

    - Plan step interpretation
    - Capability mapping
    - Input parameter preparation
    - Permission requirement mapping
    - Risk metadata propagation
    - Success criteria propagation
    - Recovery strategy propagation
    - Execution proposal synthesis

    The Execution Proposal Builder represents the transition boundary
    between strategic planning and executable actions.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Produce deterministic execution proposals
    - Remain free of observable side effects

    Implementations shall not:

    - Execute tools
    - Invoke agents
    - Perform provider routing
    - Construct provider-specific prompts
    - Authorize execution
    - Enforce permissions
    - Execute external actions
    """

    @abstractmethod
    async def build_proposal(
        self,
        plan: PlanProposal,
        step: ProposedPlanStep,
    ) -> ExecutionProposal:
        """
        Build an execution proposal for a single plan step.

        Implementations transform a validated planning step into a
        structured provider-independent ExecutionProposal suitable for
        downstream decision and execution processing.

        Args:
            plan:
                The originating plan proposal.
            step:
                The plan step requiring execution.

        Returns:
            A provider-independent ExecutionProposal.
        """

        raise NotImplementedError
