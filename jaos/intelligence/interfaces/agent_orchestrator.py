"""Agent orchestration contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.agent_descriptor import (
    AgentDescriptor,
)
from jaos.intelligence.models.agent_result import (
    AgentResult,
)
from jaos.intelligence.models.agent_task import (
    AgentTask,
)


class AgentOrchestrator(IntelligenceComponent):
    """
    Defines the provider-independent contract for agent orchestration.

    The Agent Orchestrator is responsible exclusively for coordinating
    registered intelligence agents, routing work based on capabilities,
    and tracking task execution state.

    Implementations perform orchestration activities such as:

    - Agent registration
    - Agent discovery
    - Capability matching
    - Task routing
    - Delegation coordination
    - Task state tracking
    - Result recording
    - Result retrieval

    The Agent Orchestrator represents the multi-agent coordination
    boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Coordinate registered intelligence agents
    - Preserve task lifecycle integrity
    - Remain free of observable side effects outside orchestration state

    Implementations shall not:

    - Perform reasoning
    - Generate execution plans
    - Execute tools
    - Construct provider-specific prompts
    - Perform provider routing
    - Enforce execution policies
    - Execute external actions
    """

    @abstractmethod
    async def register_agent(
        self,
        descriptor: AgentDescriptor,
    ) -> None:
        """
        Register an intelligence agent.

        Args:
            descriptor:
                The agent descriptor to register.
        """

        raise NotImplementedError

    @abstractmethod
    async def unregister_agent(
        self,
        agent_id: str,
    ) -> None:
        """
        Remove a registered intelligence agent.

        Args:
            agent_id:
                The unique agent identifier.
        """

        raise NotImplementedError

    @abstractmethod
    async def find_agents(
        self,
        required_capability: str,
    ) -> tuple[AgentDescriptor, ...]:
        """
        Find eligible agents for a required capability.

        Args:
            required_capability:
                The required capability identifier.

        Returns:
            A tuple of eligible AgentDescriptor instances.
        """

        raise NotImplementedError

    @abstractmethod
    async def route_task(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Route a task to an eligible agent.

        Args:
            task:
                The task awaiting assignment.

        Returns:
            The updated AgentTask reflecting routing decisions.
        """

        raise NotImplementedError

    @abstractmethod
    async def record_result(
        self,
        result: AgentResult,
    ) -> None:
        """
        Record the terminal result of an agent task.

        Args:
            result:
                The completed agent result.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_result(
        self,
        task_id: str,
    ) -> AgentResult | None:
        """
        Retrieve the recorded result for a task.

        Args:
            task_id:
                The unique task identifier.

        Returns:
            The recorded AgentResult when available; otherwise None.
        """

        raise NotImplementedError
