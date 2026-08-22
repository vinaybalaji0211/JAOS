"""FORTRESS-02I collection containment evidence.

Every check runs pytest in a subprocess against a synthetic tree built
under ``tmp_path``. The real preserved legacy scripts are never invoked and
never used as mutation experiments; the synthetic stand-in carries the
import-time side effect instead.

The shipped ``tests/conftest.py`` is copied verbatim into each synthetic
tree, so these tests exercise the real mechanism rather than a reimplementation.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_REAL_TESTS_CONFTEST = _REPOSITORY_ROOT / "tests" / "conftest.py"

_SIDE_EFFECT_MARKER = "SYNTHETIC_SIDE_EFFECT_FIRED"

_LEGACY_SCRIPT_SOURCE = f"""\
# Synthetic stand-in for a preserved legacy module-body script.
from pathlib import Path

Path({_SIDE_EFFECT_MARKER!r}).write_text("fired", encoding="utf-8")
"""

_CANONICAL_TEST_SOURCE = """\
def test_canonical_probe_runs():
    assert True
"""


def _build_synthetic_tree(root: Path, *, include_testpaths: bool) -> None:
    testpaths_line = "testpaths = tests/tests\n" if include_testpaths else ""
    (root / "pytest.ini").write_text(
        "[pytest]\npythonpath = .\n" + testpaths_line,
        encoding="utf-8",
    )

    tests_root = root / "tests"
    canonical_root = tests_root / "tests"
    canonical_root.mkdir(parents=True, exist_ok=True)

    (tests_root / "__init__.py").write_text("", encoding="utf-8")
    (tests_root / "conftest.py").write_text(
        _REAL_TESTS_CONFTEST.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tests_root / "legacy_side_effect_test.py").write_text(
        _LEGACY_SCRIPT_SOURCE,
        encoding="utf-8",
    )
    (canonical_root / "test_canonical_probe.py").write_text(
        _CANONICAL_TEST_SOURCE,
        encoding="utf-8",
    )


def _run_pytest(root: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_CURRENT_TEST", None)

    basetemp = root / "_basetemp"

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-p",
            "no:cacheprovider",
            f"--basetemp={basetemp}",
            *arguments,
        ],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
    )


def _side_effect_fired(root: Path) -> bool:
    return (root / _SIDE_EFFECT_MARKER).exists()


def test_real_tests_conftest_is_present() -> None:
    """The mechanism under test must actually be shipped."""

    assert _REAL_TESTS_CONFTEST.is_file()

    source = _REAL_TESTS_CONFTEST.read_text(encoding="utf-8")

    assert "def pytest_ignore_collect(" in source


@pytest.mark.parametrize(
    ("label", "arguments"),
    [
        ("bare", []),
        ("tests-directory", ["tests/"]),
        ("repository-root", ["."]),
    ],
)
def test_directory_invocations_do_not_import_legacy_scripts(
    tmp_path: Path,
    label: str,
    arguments: list[str],
    protected_repository_state: None,
) -> None:
    """F2, F3: legacy scripts are ignored before import; canonical survives."""

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(tmp_path, [*arguments, "--collect-only", "-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert not _side_effect_fired(tmp_path), (
        f"{label}: the legacy module body executed"
    )
    assert "test_canonical_probe" in result.stdout
    assert "legacy_side_effect_test" not in result.stdout


def test_canonical_tests_still_execute(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F1, A2: the boundary does not mask the canonical tree."""

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(tmp_path, ["-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
    assert not _side_effect_fired(tmp_path)


def test_containment_does_not_depend_on_testpaths(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F6: the boundary holds with no testpaths configured at all."""

    _build_synthetic_tree(tmp_path, include_testpaths=False)

    result = _run_pytest(tmp_path, ["tests/", "--collect-only", "-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert not _side_effect_fired(tmp_path)
    assert "test_canonical_probe" in result.stdout


def test_explicit_legacy_path_invocation_still_imports(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F4, F5: documented pytest limitation, proven with evidence.

    pytest resolves a directly-named argument to a module before consulting
    ``pytest_ignore_collect``, so the module body runs. No conftest-level
    mechanism prevents this. Collection still yields nothing (exit code 5),
    and certification commands therefore always target ``tests/tests``.
    """

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(
        tmp_path,
        ["tests/legacy_side_effect_test.py", "--collect-only", "-q"],
    )

    assert _side_effect_fired(tmp_path), (
        "the documented limitation no longer reproduces; the boundary may "
        "now be stronger than recorded and this test needs review"
    )
    assert result.returncode == 5
    assert "no tests" in result.stdout.lower()


@pytest.mark.parametrize(
    "ignore_argument",
    [
        "--ignore-glob=*/tests/*_test.py",
        "--ignore=tests/legacy_side_effect_test.py",
    ],
)
def test_ignore_options_also_cannot_block_explicit_paths(
    tmp_path: Path,
    ignore_argument: str,
    protected_repository_state: None,
) -> None:
    """F5: --ignore and --ignore-glob do not close the explicit-path gap.

    This is the evidence that modifying pytest.ini would not help, which is
    why FORTRESS-02I leaves pytest.ini unchanged.
    """

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(
        tmp_path,
        [
            ignore_argument,
            "tests/legacy_side_effect_test.py",
            "--collect-only",
            "-q",
        ],
    )

    assert _side_effect_fired(tmp_path)
    assert result.returncode == 5


def test_certification_target_never_reaches_legacy_scripts(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """The certification command shape cannot trigger the limitation."""

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(tmp_path, ["tests/tests", "-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert not _side_effect_fired(tmp_path)
    assert "1 passed" in result.stdout


def test_no_environment_variable_is_persistently_mutated(
    tmp_path: Path,
) -> None:
    """F7: the focused tests leave the parent environment untouched."""

    before = dict(os.environ)

    _build_synthetic_tree(tmp_path, include_testpaths=True)
    _run_pytest(tmp_path, ["--collect-only", "-q"])

    assert dict(os.environ) == before


def test_collection_boundary_classifies_paths_correctly() -> None:
    """A2: the boundary predicate retains support files and the canonical tree."""

    specification = importlib.util.spec_from_file_location(
        "fortress_02i_tests_conftest_probe",
        _REAL_TESTS_CONFTEST,
    )
    assert specification is not None
    assert specification.loader is not None

    tests_conftest = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(tests_conftest)

    tests_root = _REPOSITORY_ROOT / "tests"

    assert tests_conftest.is_excluded_legacy_module(
        tests_root / "goal_tracker_test.py"
    )
    assert tests_conftest.is_excluded_legacy_module(
        tests_root / "test_runner.py"
    )
    assert not tests_conftest.is_excluded_legacy_module(
        tests_root / "__init__.py"
    )
    assert not tests_conftest.is_excluded_legacy_module(
        tests_root / "conftest.py"
    )
    assert not tests_conftest.is_excluded_legacy_module(
        tests_root / "tests" / "platform" / "test_runtime_paths.py"
    )
