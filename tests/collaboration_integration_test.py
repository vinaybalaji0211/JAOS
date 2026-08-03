from brain.agent_collaboration_core import AgentCollaborationCore
from brain.agent_communication_bus import AgentCommunicationBus
from brain.consensus_engine import ConsensusEngine
from brain.multi_agent_coordinator import MultiAgentCoordinator
from brain.shared_task_manager import SharedTaskManager
from brain.task_delegation_engine import TaskDelegationEngine

print(
    "\n=== AGENT COLLABORATION INTEGRATION TEST ===\n"
)

# Collaboration Core

core = AgentCollaborationCore()

core.start_collaboration(
    "Analyze Quantum Research",
    [
        "ResearchAgent",
        "DocumentAgent",
        "MemoryAgent"
    ]
)

core.show_collaborations()

# Shared Task Manager

tasks = SharedTaskManager()

tasks.create_task(
    "Analyze Quantum Research",
    [
        "ResearchAgent",
        "DocumentAgent"
    ]
)

tasks.update_status(
    "Analyze Quantum Research",
    "IN_PROGRESS"
)

tasks.show_tasks()

# Communication Bus

bus = AgentCommunicationBus()

bus.send_message(
    "ResearchAgent",
    "DocumentAgent",
    "Extract key concepts."
)

bus.show_messages()

# Delegation

delegation = TaskDelegationEngine()

delegation.delegate_task(
    "Extract Key Concepts",
    "ResearchAgent",
    "DocumentAgent"
)

delegation.complete_task(
    "Extract Key Concepts"
)

delegation.show_delegations()

# Consensus

consensus = ConsensusEngine()

consensus.vote(
    "Publish Report",
    "ResearchAgent",
    "YES"
)

consensus.vote(
    "Publish Report",
    "MemoryAgent",
    "YES"
)

consensus.vote(
    "Publish Report",
    "SecurityAgent",
    "NO"
)

consensus.show_votes()

# Coordinator

coordinator = (
    MultiAgentCoordinator()
)

coordinator.create_project(
    "Quantum Research Analysis",
    [
        "ResearchAgent",
        "DocumentAgent",
        "MemoryAgent"
    ]
)

coordinator.complete_project(
    "Quantum Research Analysis"
)

coordinator.show_projects()

print(
    "\n=== AGENT COLLABORATION COMPLETE ==="
)