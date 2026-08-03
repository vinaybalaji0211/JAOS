"""Decision strategy definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from enum import Enum


class DecisionStrategy(str, Enum):
    """
    Defines the high-level decision strategy used by the
    Decision Engine.

    The decision strategy determines how candidate plans
    are evaluated and selected. It influences only the
    decision methodology and does not control execution,
    provider routing, or external actions.
    """

    DIRECT = "direct"
    """Select the most straightforward valid decision."""

    RISK_AWARE = "risk_aware"
    """Prioritize decisions that minimize operational and security risks."""

    POLICY_FIRST = "policy_first"
    """Evaluate organizational and security policies before selecting a decision."""

    ADAPTIVE = "adaptive"
    """Select the decision strategy dynamically based on context, permissions, risk, and available capabilities."""
