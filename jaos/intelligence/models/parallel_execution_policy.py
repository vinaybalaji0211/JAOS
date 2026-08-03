"""Parallel execution policy definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from enum import Enum


class ParallelExecutionPolicy(str, Enum):
    """
    Defines how the Planning Engine may introduce parallelism
    while constructing an execution graph.

    The parallel execution policy governs only planning-time
    decomposition and dependency analysis. It does not authorize
    concurrent execution of plan steps.

    Execution concurrency remains the responsibility of the
    Executive Platform.
    """

    SEQUENTIAL = "sequential"
    """
    Produce a strictly linear planning graph where each step
    depends on completion of the previous step.
    """

    PARALLEL = "parallel"
    """
    Produce planning graphs that maximize parallel branches
    whenever dependency analysis determines it is safe.
    """

    AUTO = "auto"
    """
    Allow the Planning Engine to determine the appropriate
    degree of parallelism based on dependencies, constraints,
    complexity, and planning context.
    """
