"""Agent orchestration contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.agent_descriptor import AgentDescriptor
from jaos.intelligence.models.agent_result import AgentResult
from jaos.intelligence.models.agent_task import AgentTask


class AgentOrchestrator(IntelligenceComponent):
    """
    Defines agent discovery, registration, routing, and result tracking.

    Implementations must enforce capability matching, availability,
    health, delegation depth, identity, permissions, resource limits,
    and task-state transitions.
    """

    @abstractmethod
    def register_agent(self, descriptor: AgentDescriptor) -> None:
        """Register an agent descriptor with the orchestrator."""

        raise NotImplementedError

    @abstractmethod
    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent registration."""

        raise NotImplementedError

    @abstractmethod
    def find_agents(
        self,
        required_capability: str,
    ) -> tuple[AgentDescriptor, ...]:
        """Return eligible agents for a required capability."""

        raise NotImplementedError

    @abstractmethod
    def route_task(self, task: AgentTask) -> AgentTask:
        """Route a pending task and return its updated task snapshot."""

        raise NotImplementedError

    @abstractmethod
    def record_result(self, result: AgentResult) -> None:
        """Record a terminal result returned by an assigned agent."""

        raise NotImplementedError

    @abstractmethod
    def get_result(self, task_id: str) -> AgentResult | None:
        """Return the recorded result for a task when available."""

        raise NotImplementedError