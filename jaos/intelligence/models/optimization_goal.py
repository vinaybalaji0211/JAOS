"""Optimization goal definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from enum import Enum


class OptimizationGoal(str, Enum):
    """
    Defines the primary optimization objective for the
    Planning Engine.

    The optimization goal influences how the Planning
    Engine balances competing planning trade-offs while
    constructing an execution graph.

    This enumeration governs planning behavior only.
    It does not influence execution policy, provider
    routing, or runtime scheduling.
    """

    BALANCED = "balanced"
    """
    Produce a balanced execution plan that considers
    time, cost, reliability, and overall planning quality.
    """

    MINIMIZE_TIME = "minimize_time"
    """
    Prioritize planning strategies that reduce total
    execution time, favoring safe parallelism whenever
    possible.
    """

    MINIMIZE_COST = "minimize_cost"
    """
    Prioritize planning strategies that reduce resource
    consumption and execution cost while maintaining
    acceptable plan quality.
    """

    MAXIMIZE_RELIABILITY = "maximize_reliability"
    """
    Prioritize planning strategies that maximize
    robustness through additional validation,
    redundancy, and contingency planning.
    """
