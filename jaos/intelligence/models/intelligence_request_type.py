"""Request types for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class IntelligenceRequestType(str, Enum):
    """Classifies a high-level intelligence operation."""

    CONVERSATION = "conversation"
    CONTEXT = "context"
    REASONING = "reasoning"
    PLANNING = "planning"
    AGENT_TASK = "agent_task"
    EXECUTION_PROPOSAL = "execution_proposal"