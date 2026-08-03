"""Fallback policy definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from enum import Enum


class FallbackPolicy(str, Enum):
    """
    Defines how the Planning Engine generates contingency
    strategies while constructing a planning graph.

    A fallback policy governs only the generation of
    alternative planning paths. It does not authorize or
    execute fallback behavior.

    Fallback execution remains the responsibility of the
    Executive Platform after approval by the Decision Engine.
    """

    DISABLED = "disabled"
    """
    Do not generate fallback branches or contingency
    planning paths.
    """

    REACTIVE = "reactive"
    """
    Generate contingency strategies that may be invoked
    after an execution failure is detected.
    """

    PROACTIVE = "proactive"
    """
    Generate contingency branches during planning for
    high-risk or high-uncertainty operations.
    """
