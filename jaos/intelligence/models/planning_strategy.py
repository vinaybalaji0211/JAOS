"""Planning strategy definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from enum import Enum


class PlanningStrategy(str, Enum):
    """
    Defines the high-level planning strategy used by the
    Planning Engine.

    The planning strategy determines how cognitive understanding
    is transformed into an execution plan. It influences only
    planning methodology and does not control execution,
    optimization, or fallback behavior.
    """

    DIRECT = "direct"
    """Generate a straightforward linear execution plan."""

    HIERARCHICAL = "hierarchical"
    """Generate a hierarchical plan by decomposing objectives into sub-goals."""

    ADAPTIVE = "adaptive"
    """Select the planning approach dynamically based on planning context."""
