"""Execution proposal builder contract for JAOS Intelligence."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.execution_proposal import ExecutionProposal
from jaos.intelligence.models.plan_proposal import PlanProposal
from jaos.intelligence.models.proposed_plan_step import ProposedPlanStep


class ExecutionProposalBuilder(IntelligenceComponent):
    """
    Defines conversion from plan steps to execution proposals.

    Implementations translate planning output into validated capability,
    input, permission, risk, success, and recovery contracts. They do
    not authorize proposals or invoke agents, tools, or system services.
    """

    @abstractmethod
    def build_proposal(
        self,
        plan: PlanProposal,
        step: ProposedPlanStep,
    ) -> ExecutionProposal:
        """Build an execution proposal for one step in a plan."""

        raise NotImplementedError
