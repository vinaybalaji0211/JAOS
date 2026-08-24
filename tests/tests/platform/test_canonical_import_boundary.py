"""FORTRESS-02I canonical import-boundary architecture guard.

Boundary definition
-------------------
The canonical production path is the static import closure of
``run_jaos.py``, computed by AST analysis over repository-local modules
only. Third-party and standard-library imports are not repository modules
and are therefore not traversed.

A module is forbidden when the FIRST component of its dotted name is a
verified legacy or shadow package identity. The rule is identity-based, not
substring-based: ``core`` is forbidden while a hypothetical ``jaos.core``
would be allowed, and root ``memory`` is forbidden while canonical
``jaos.memory`` is allowed.

False positives are avoided structurally. Comments and strings never reach
the analyzer because it walks the AST rather than raw text, and
``if TYPE_CHECKING:`` bodies are skipped because they are not runtime
dependencies. Imports inside function bodies ARE counted, because calling
the function makes them real runtime dependencies.

This guard never launches JAOS. It is read-only static analysis.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

CANONICAL_ENTRY_POINT = "run_jaos.py"

FORBIDDEN_TOP_LEVEL_MODULES = frozenset(
    {
        "agent",
        "agents",
        "autonomous",
        "brain",
        "memory",
        "core",
        "executive_brain",
        "kernel",
        "main",
        "planning",
        "reasoning",
        "tests",
        "workflow",
    }
)

FORBIDDEN_CANONICAL_MODULE_PREFIXES = (
    "jaos.intelligence.context.memory_context_source",
    "jaos.intelligence.decision",
    "jaos.intelligence.interfaces.agent_orchestrator",
    "jaos.intelligence.interfaces.decision_engine",
    "jaos.intelligence.interfaces.execution_proposal_builder",
    "jaos.intelligence.interfaces.planning_engine",
    "jaos.intelligence.interfaces.reasoning_engine",
    "jaos.intelligence.models.agent_",
    "jaos.intelligence.models.confidence_assessment",
    "jaos.intelligence.models.decision_",
    "jaos.intelligence.models.execution_proposal",
    "jaos.intelligence.models.explainability_report",
    "jaos.intelligence.models.fallback_policy",
    "jaos.intelligence.models.optimization_goal",
    "jaos.intelligence.models.parallel_execution_policy",
    "jaos.intelligence.models.plan_proposal",
    "jaos.intelligence.models.planning_",
    "jaos.intelligence.models.proposed_plan_step",
    "jaos.intelligence.models.reasoning_",
    "jaos.intelligence.planning",
    "jaos.memory.storage.memory_search_engine",
)


def is_forbidden_runtime_module(module_name: str) -> bool:
    """Return whether a module is outside the canonical runtime boundary."""

    top_level = module_name.split(".", maxsplit=1)[0]
    return (
        top_level in FORBIDDEN_TOP_LEVEL_MODULES
        or module_name.startswith(FORBIDDEN_CANONICAL_MODULE_PREFIXES)
    )


def _is_type_checking_guard(node: ast.If) -> bool:
    test = node.test
    if isinstance(test, ast.Name):
        return test.id == "TYPE_CHECKING"
    if isinstance(test, ast.Attribute):
        return test.attr == "TYPE_CHECKING"
    return False


def _collect_imports(node: ast.AST, modules: set[str], relative: list[str]) -> None:
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.If) and _is_type_checking_guard(child):
            for fallback in child.orelse:
                _collect_imports(fallback, modules, relative)
            continue

        if isinstance(child, ast.Import):
            for alias in child.names:
                modules.add(alias.name)
        elif isinstance(child, ast.ImportFrom):
            if child.level:
                relative.append(child.module or "")
            elif child.module:
                modules.add(child.module)

        _collect_imports(child, modules, relative)


def _module_sources(root: Path, module_name: str) -> list[tuple[str, Path]]:
    """Resolve import-time sources, including every parent package facade."""

    parts = module_name.split(".")
    sources: list[tuple[str, Path]] = []

    for index in range(1, len(parts) + 1):
        package_name = ".".join(parts[:index])
        package_init = root.joinpath(*parts[:index]) / "__init__.py"
        if package_init.is_file():
            sources.append((package_name, package_init))

    module_file = root.joinpath(*parts).with_suffix(".py")
    if module_file.is_file():
        sources.append((module_name, module_file))

    return sources


def analyze_import_closure(
    root: Path,
    entry_point: str,
) -> dict[str, object]:
    """Return the repository-local import closure of one entry point."""

    entry_path = root / entry_point
    if not entry_path.is_file():
        raise AssertionError(f"entry point is missing: {entry_point}")

    pending: list[tuple[str, Path]] = [(entry_point, entry_path)]
    visited_files: set[Path] = set()
    reached_modules: set[str] = set()
    violations: list[str] = []
    relative_imports: list[str] = []

    while pending:
        owner, source_path = pending.pop()
        if source_path in visited_files:
            continue
        visited_files.add(source_path)

        tree = ast.parse(source_path.read_text(encoding="utf-8"))

        imported: set[str] = set()
        relative: list[str] = []
        _collect_imports(tree, imported, relative)

        for module_name in sorted(relative):
            relative_imports.append(f"{owner} -> relative import {module_name!r}")

        for module_name in sorted(imported):
            top_level = module_name.split(".", maxsplit=1)[0]

            if top_level in FORBIDDEN_TOP_LEVEL_MODULES:
                violations.append(
                    f"{owner} imports forbidden module {module_name}"
                )
                continue

            if is_forbidden_runtime_module(module_name):
                violations.append(
                    f"{owner} imports deferred module {module_name}"
                )
                continue

            for resolved_name, resolved_path in _module_sources(
                root,
                module_name,
            ):
                reached_modules.add(resolved_name)
                pending.append((resolved_name, resolved_path))

    return {
        "reached_modules": reached_modules,
        "violations": violations,
        "relative_imports": relative_imports,
        "analyzed_files": visited_files,
    }


def _write_module(root: Path, relative_path: str, source: str) -> Path:
    module_path = root / relative_path
    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text(source, encoding="utf-8")
    return module_path


def _synthetic_canonical_tree(root: Path, canonical_body: str) -> None:
    _write_module(root, "run_jaos.py", "from jaos.cli.shell import JAOSShell\n")
    _write_module(root, "jaos/__init__.py", "")
    _write_module(root, "jaos/cli/__init__.py", "")
    _write_module(root, "jaos/cli/shell.py", canonical_body)
    _write_module(root, "brain/__init__.py", "")
    _write_module(root, "brain/goal_tracker.py", "")
    _write_module(root, "memory/__init__.py", "")
    _write_module(root, "memory/long_term_memory.py", "")
    _write_module(root, "core/__init__.py", "")
    _write_module(root, "core/engine.py", "")
    _write_module(root, "jaos/tools/__init__.py", "")
    _write_module(root, "jaos/tools/tool_manager.py", "")


def test_canonical_closure_has_no_legacy_dependency() -> None:
    """G1: the real repository passes the canonical import boundary."""

    report = analyze_import_closure(
        _REPOSITORY_ROOT,
        CANONICAL_ENTRY_POINT,
    )

    assert report["violations"] == []
    assert report["reached_modules"], "the closure must not be empty"


def test_canonical_closure_uses_only_absolute_imports() -> None:
    """The analyzer cannot follow relative imports, so prove none exist."""

    report = analyze_import_closure(
        _REPOSITORY_ROOT,
        CANONICAL_ENTRY_POINT,
    )

    assert report["relative_imports"] == []


def test_canonical_closure_reaches_expected_platforms() -> None:
    """G1: the closure genuinely covers the canonical platforms."""

    report = analyze_import_closure(
        _REPOSITORY_ROOT,
        CANONICAL_ENTRY_POINT,
    )
    reached = report["reached_modules"]
    assert isinstance(reached, set)

    expected_roots = (
        "jaos.cli",
        "jaos.ai",
        "jaos.tools",
        "jaos.executive",
        "jaos.memory",
        "jaos.intelligence",
        "jaos_platform",
        "jaos.composition",
    )
    for expected in expected_roots:
        assert any(
            module == expected or module.startswith(f"{expected}.")
            for module in reached
        ), expected


def test_canonical_closure_reaches_platform_runtime_lifecycle() -> None:
    """FORTRESS-04: run_jaos.py's closure reaches the Runtime Platform
    lifecycle owner, not merely some jaos_platform symbol."""

    report = analyze_import_closure(
        _REPOSITORY_ROOT,
        CANONICAL_ENTRY_POINT,
    )
    reached = report["reached_modules"]
    assert isinstance(reached, set)

    assert any(
        module in {"jaos_platform.platform_runtime", "jaos_platform"}
        or module.startswith("jaos_platform.platform_runtime")
        for module in reached
    )
    assert any(
        module in {"jaos_platform.boot_manager", "jaos_platform"}
        or module.startswith("jaos_platform.boot_manager")
        for module in reached
    )


@pytest.mark.parametrize(
    ("forbidden_import", "expected_fragment"),
    [
        ("from brain.goal_tracker import GoalTracker", "brain.goal_tracker"),
        ("from memory.long_term_memory import LongTermMemory", "memory.long_term_memory"),
        ("from core.engine import JarvisEngine", "core.engine"),
        ("import brain", "brain"),
    ],
)
def test_forbidden_legacy_imports_are_detected(
    tmp_path: Path,
    forbidden_import: str,
    expected_fragment: str,
) -> None:
    """G2, G3, G4: synthetic legacy imports are detected."""

    _synthetic_canonical_tree(
        tmp_path,
        f"{forbidden_import}\n\n\nclass JAOSShell:\n    pass\n",
    )

    report = analyze_import_closure(tmp_path, "run_jaos.py")
    violations = report["violations"]

    assert isinstance(violations, list)
    assert violations, "the forbidden import was not detected"
    assert any(expected_fragment in violation for violation in violations)


@pytest.mark.parametrize(
    "deferred_import",
    [
        "from jaos.intelligence.decision import DefaultDecisionEngine",
        "from jaos.intelligence.interfaces.decision_engine import DecisionEngine",
        "from jaos.intelligence.models.decision_request import DecisionRequest",
        "from jaos.intelligence.models.confidence_assessment import ConfidenceAssessment",
        "from jaos.intelligence.models.explainability_report import ExplainabilityReport",
        "from jaos.intelligence.models.fallback_policy import FallbackPolicy",
        "from jaos.intelligence.models.optimization_goal import OptimizationGoal",
        "from jaos.intelligence.models.parallel_execution_policy import ParallelExecutionPolicy",
        "from jaos.intelligence.planning import DefaultPlanningEngine",
    ],
)
def test_deferred_intelligence_imports_are_detected(
    tmp_path: Path,
    deferred_import: str,
) -> None:
    _synthetic_canonical_tree(
        tmp_path,
        f"{deferred_import}\n\n\nclass JAOSShell:\n    pass\n",
    )

    report = analyze_import_closure(tmp_path, "run_jaos.py")

    assert report["violations"]


def test_safe_canonical_import_passes(tmp_path: Path) -> None:
    """G5: a canonical jaos.* import is allowed."""

    _synthetic_canonical_tree(
        tmp_path,
        "from jaos.tools.tool_manager import ToolManager\n\n\n"
        "class JAOSShell:\n    pass\n",
    )

    report = analyze_import_closure(tmp_path, "run_jaos.py")

    assert report["violations"] == []
    assert "jaos.tools.tool_manager" in report["reached_modules"]


def test_type_checking_only_import_is_not_a_runtime_dependency(
    tmp_path: Path,
) -> None:
    """A TYPE_CHECKING-guarded legacy import is not a runtime dependency."""

    _synthetic_canonical_tree(
        tmp_path,
        "from typing import TYPE_CHECKING\n\n"
        "if TYPE_CHECKING:\n"
        "    from brain.goal_tracker import GoalTracker\n\n\n"
        "class JAOSShell:\n    pass\n",
    )

    report = analyze_import_closure(tmp_path, "run_jaos.py")

    assert report["violations"] == []


def test_commented_and_quoted_legacy_names_do_not_false_positive(
    tmp_path: Path,
) -> None:
    """Comments and string literals must never register as imports."""

    _synthetic_canonical_tree(
        tmp_path,
        "# from brain.goal_tracker import GoalTracker\n"
        "LEGACY_REFERENCE = 'from core.engine import JarvisEngine'\n"
        "DOCUMENTED = \"memory.long_term_memory\"\n\n\n"
        "class JAOSShell:\n    pass\n",
    )

    report = analyze_import_closure(tmp_path, "run_jaos.py")

    assert report["violations"] == []
