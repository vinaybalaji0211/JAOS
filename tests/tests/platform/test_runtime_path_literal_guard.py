"""FORTRESS-02I internal runtime path-literal architecture guard.

Boundary definition
-------------------
Scope is canonical production code only: ``jaos/`` and ``jaos_platform/``.
Preserved legacy and quarantine sources (``brain/``, root ``memory/``,
``core/``, ``executive_brain/``, ``kernel/``, ``scripts/``), documentation,
and tests are out of scope — they are governed by FORTRESS-06, not here.

A violation is a string literal that names a repository-relative JAOS
INTERNAL mutable runtime-state location: anything under ``data/``,
``logs/``, or ``exports/``, or the mutable configuration files
``config/settings.json`` and ``config/providers.json``.

Deliberate exclusions:

* ``jaos_platform/runtime_state_inventory.py`` — its literals are read-only
  descriptors of preserved legacy artifacts beneath an injected source
  root, not runtime write targets. The exclusion is proven meaningful by
  ``test_inventory_descriptors_would_otherwise_be_flagged``.
* User-directed filesystem tool paths, which come from a caller-supplied
  payload and contain no literal at all.
* Approved read-only repository defaults are permitted only where the
  literal is not one of the mutable configuration targets above.

Literals are gathered by AST inspection, so comments never register.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

CANONICAL_SOURCE_ROOTS = (
    "jaos",
    "jaos_platform",
)

EXCLUDED_CANONICAL_SOURCES = frozenset(
    {
        "jaos_platform/runtime_state_inventory.py",
    }
)

FORBIDDEN_STATE_PREFIXES = (
    "data/",
    "logs/",
    "exports/",
)

FORBIDDEN_MUTABLE_CONFIGURATION = frozenset(
    {
        "config/settings.json",
        "config/providers.json",
    }
)


def _is_forbidden_literal(value: str) -> bool:
    normalized = value.replace("\\", "/").strip()

    if normalized in FORBIDDEN_MUTABLE_CONFIGURATION:
        return True

    return any(
        normalized.startswith(prefix)
        for prefix in FORBIDDEN_STATE_PREFIXES
    )


def _string_literals(source_path: Path) -> list[str]:
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]


def scan_repository_relative_state_literals(
    root: Path,
    source_roots: tuple[str, ...] = CANONICAL_SOURCE_ROOTS,
    excluded_sources: frozenset[str] = EXCLUDED_CANONICAL_SOURCES,
) -> list[str]:
    """Return violations of the internal runtime path-literal boundary."""

    violations: list[str] = []

    for source_root in source_roots:
        root_path = root / source_root
        if not root_path.is_dir():
            continue

        for source_path in sorted(root_path.rglob("*.py")):
            relative_path = source_path.relative_to(root).as_posix()
            if relative_path in excluded_sources:
                continue

            for literal in _string_literals(source_path):
                if _is_forbidden_literal(literal):
                    violations.append(f"{relative_path}: {literal!r}")

    return violations


def _write_module(root: Path, relative_path: str, source: str) -> Path:
    module_path = root / relative_path
    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text(source, encoding="utf-8")
    return module_path


def test_canonical_sources_declare_no_internal_state_literals() -> None:
    """G1: the real canonical packages pass the boundary."""

    violations = scan_repository_relative_state_literals(_REPOSITORY_ROOT)

    assert violations == []


def test_inventory_descriptors_would_otherwise_be_flagged() -> None:
    """G8: the inventory exclusion is real, narrow, and load-bearing."""

    inventory_relative = "jaos_platform/runtime_state_inventory.py"
    inventory_path = _REPOSITORY_ROOT / inventory_relative

    if not inventory_path.is_file():
        pytest.skip("the legacy runtime-state inventory is absent")

    without_exclusion = scan_repository_relative_state_literals(
        _REPOSITORY_ROOT,
        excluded_sources=frozenset(),
    )

    assert without_exclusion, "the exclusion protects nothing"
    assert all(
        violation.startswith(inventory_relative)
        for violation in without_exclusion
    ), without_exclusion


@pytest.mark.parametrize(
    "forbidden_literal",
    [
        "data/behavior/behavior_patterns.json",
        "data/decisions/decision_records.json",
        "data/goals/goals.json",
        "data/memory/long_term_memory.json",
        "data/providers/provider_memory.json",
        "data/reasoning/reasoning_traces.json",
        "data/recovery/crash_checkpoint.json",
        "data/history/actions.json",
        "data/snapshots",
        "data/backups",
        "logs/system.log",
        "exports/",
        "config/settings.json",
        "config/providers.json",
    ],
)
def test_forbidden_state_literals_are_detected(
    tmp_path: Path,
    forbidden_literal: str,
) -> None:
    """G6: a new repository-relative internal-state default is detected."""

    _write_module(
        tmp_path,
        "jaos/persistence/legacy_writer.py",
        f'STATE_PATH = "{forbidden_literal}"\n',
    )

    violations = scan_repository_relative_state_literals(tmp_path)

    assert violations, forbidden_literal
    assert any(forbidden_literal in violation for violation in violations)


def test_runtime_paths_usage_passes(tmp_path: Path) -> None:
    """G7: composing paths from injected RuntimePaths is allowed."""

    _write_module(
        tmp_path,
        "jaos/persistence/canonical_writer.py",
        "from pathlib import Path\n\n"
        "DATABASE_FILENAME = 'memory.sqlite3'\n\n\n"
        "def build_database_path(runtime_paths) -> Path:\n"
        "    return runtime_paths.memory / DATABASE_FILENAME\n",
    )

    violations = scan_repository_relative_state_literals(tmp_path)

    assert violations == []


def test_user_directed_tool_paths_pass(tmp_path: Path) -> None:
    """G9: caller-supplied filesystem tool paths are not violations."""

    _write_module(
        tmp_path,
        "jaos/tools/filesystem/write_file_tool.py",
        "from pathlib import Path\n\n\n"
        "class WriteFileTool:\n"
        "    def execute(self, request):\n"
        "        target = Path(request.payload['path'])\n"
        "        target.parent.mkdir(parents=True, exist_ok=True)\n"
        "        target.write_text(request.payload['content'], encoding='utf-8')\n"
        "        return target\n",
    )

    violations = scan_repository_relative_state_literals(tmp_path)

    assert violations == []


def test_documentation_and_tests_are_out_of_scope(tmp_path: Path) -> None:
    """Legacy, documentation, and test sources are not scanned."""

    _write_module(
        tmp_path,
        "brain/behavior_tracker.py",
        'FILE_PATH = "data/behavior/behavior_patterns.json"\n',
    )
    _write_module(
        tmp_path,
        "tests/tests/platform/test_example.py",
        'LITERAL = "data/goals/goals.json"\n',
    )
    _write_module(
        tmp_path,
        "jaos/__init__.py",
        "",
    )

    violations = scan_repository_relative_state_literals(tmp_path)

    assert violations == []


def test_comments_do_not_false_positive(tmp_path: Path) -> None:
    """AST inspection means a commented path is never a violation."""

    _write_module(
        tmp_path,
        "jaos/persistence/documented.py",
        "# Legacy default was data/memory/long_term_memory.json\n"
        "VALUE = 1\n",
    )

    violations = scan_repository_relative_state_literals(tmp_path)

    assert violations == []
