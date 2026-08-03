"""Failure behavior enumeration for the JAOS AI Intelligence Platform."""

from enum import Enum


class FailureBehavior(str, Enum):
    """Defines planner behavior when a plan step fails."""

    STOP = "stop"
    CONTINUE = "continue"
    RETRY = "retry"
    ESCALATE = "escalate"
