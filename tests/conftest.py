"""FORTRESS-02I collection boundary for the whole ``tests/`` tree.

The preserved legacy scripts directly beneath ``tests/`` are module-body
programs rather than pytest tests. They match pytest's default
``python_files`` patterns, so any directory-based invocation would import
and execute them, writing into protected repository runtime state.

This conftest excludes them before import for every directory-based
invocation (``pytest``, ``pytest tests/``, ``pytest .``). The canonical
tree at ``tests/tests`` is never affected.

Known pytest limitation, proven by
``tests/tests/platform/test_collection_containment.py``: naming an excluded
file explicitly on the command line still imports it. pytest resolves a
directly-specified argument to a module before consulting
``pytest_ignore_collect``, and ``--ignore`` / ``--ignore-glob`` behave the
same way whether supplied on the command line or through ``addopts``. No
conftest-level mechanism can prevent that, so certification commands must
always target ``tests/tests``.

The legacy files themselves are preserved untouched; quarantine belongs to
FORTRESS-06.
"""

from __future__ import annotations

from pathlib import Path


_TESTS_ROOT = Path(__file__).resolve().parent

CANONICAL_TEST_TREE = _TESTS_ROOT / "tests"

RETAINED_FLAT_FILENAMES = frozenset(
    {
        "conftest.py",
        "__init__.py",
    }
)


def is_excluded_legacy_module(candidate_path: Path) -> bool:
    """Return whether a path is a preserved legacy flat ``tests/`` script."""

    if candidate_path.suffix != ".py":
        return False

    if candidate_path.name in RETAINED_FLAT_FILENAMES:
        return False

    return candidate_path.parent == _TESTS_ROOT


def pytest_ignore_collect(collection_path, config):
    """Exclude preserved legacy flat scripts before pytest imports them."""

    candidate_path = Path(collection_path)

    if not candidate_path.is_file():
        return None

    if is_excluded_legacy_module(candidate_path):
        return True

    return None
