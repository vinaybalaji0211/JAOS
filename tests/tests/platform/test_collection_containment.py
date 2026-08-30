"""FORTRESS-02I/FORTRESS-06B collection containment evidence.

Every check runs pytest in a subprocess against a synthetic tree built
under ``tmp_path``. The real preserved legacy scripts are never invoked and
never used as mutation experiments; the synthetic stand-in carries the
import-time side effect instead.

The shipped ``pytest.ini`` and ``tests/conftest.py`` are copied into each
synthetic tree, so these tests exercise the real mechanisms rather than a
reimplementation. FORTRESS-06B also recreates the root/test ``brain`` package
collision and represents the two root artifacts as non-Python archives.
"""

from __future__ import annotations

import ast
import configparser
import fnmatch
import importlib.machinery
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_REAL_PYTEST_INI = _REPOSITORY_ROOT / "pytest.ini"
_REAL_TESTS_CONFTEST = _REPOSITORY_ROOT / "tests" / "conftest.py"
_ARCHIVE_TESTS_ROOT = _REPOSITORY_ROOT / "legacy_quarantine" / "tests"

_ARCHIVED_ARTIFACT_NAMES = frozenset(
    {
        "phase14_integration_test.py.legacy",
        "test_logger.py.legacy",
    }
)
_FORMER_ROOT_MODULE_NAMES = (
    "phase14_integration_test",
    "test_logger",
)

_SIDE_EFFECT_MARKER = "SYNTHETIC_SIDE_EFFECT_FIRED"
_ARCHIVE_SIDE_EFFECT_MARKER = "SYNTHETIC_ARCHIVE_SIDE_EFFECT_FIRED"

_LEGACY_SCRIPT_SOURCE = f"""\
# Synthetic stand-in for a preserved legacy module-body script.
from pathlib import Path

Path({_SIDE_EFFECT_MARKER!r}).write_text("fired", encoding="utf-8")
"""

_CANONICAL_TEST_SOURCE = """\
def test_canonical_probe_runs():
    assert True
"""

_COLLISION_TEST_SOURCE = """\
import sys

import brain
import jaos


def test_importlib_mode_preserves_application_package_identity():
    assert brain.ORIGIN == "root-application-brain"
    assert jaos.ORIGIN == "canonical-jaos"
    assert sys.modules["brain"] is brain
    test_module = sys.modules[__name__]
    identities = [
        name for name, module in sys.modules.items() if module is test_module
    ]
    assert identities == [__name__]
"""

_ARCHIVED_TEST_SHAPED_SOURCE = f"""\
# Synthetic stand-in for a quarantined root test-shaped artifact.
from pathlib import Path

Path({_ARCHIVE_SIDE_EFFECT_MARKER!r}).write_text("fired", encoding="utf-8")
raise AssertionError("a .py.legacy archive must never be imported")
"""


def _build_synthetic_tree(root: Path, *, include_testpaths: bool) -> None:
    configuration = _REAL_PYTEST_INI.read_text(encoding="utf-8")
    if not include_testpaths:
        configuration = "\n".join(
            line
            for line in configuration.splitlines()
            if not line.strip().startswith("testpaths")
        )
        configuration += "\n"
    (root / "pytest.ini").write_text(configuration, encoding="utf-8")

    (root / "conftest.py").write_text("import brain\n", encoding="utf-8")

    application_brain = root / "brain"
    application_brain.mkdir(parents=True, exist_ok=True)
    (application_brain / "__init__.py").write_text(
        'ORIGIN = "root-application-brain"\n',
        encoding="utf-8",
    )

    canonical_jaos = root / "jaos"
    canonical_jaos.mkdir(parents=True, exist_ok=True)
    (canonical_jaos / "__init__.py").write_text(
        'ORIGIN = "canonical-jaos"\n',
        encoding="utf-8",
    )

    tests_root = root / "tests"
    canonical_root = tests_root / "tests"
    collision_root = canonical_root / "brain"
    canonical_root.mkdir(parents=True, exist_ok=True)
    collision_root.mkdir(parents=True, exist_ok=True)

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
    (collision_root / "__init__.py").write_text("", encoding="utf-8")
    (collision_root / "test_collision_probe.py").write_text(
        _COLLISION_TEST_SOURCE,
        encoding="utf-8",
    )

    archive_root = root / "legacy_quarantine" / "tests"
    archive_root.mkdir(parents=True, exist_ok=True)
    for archived_name in _ARCHIVED_ARTIFACT_NAMES:
        (archive_root / archived_name).write_text(
            _ARCHIVED_TEST_SHAPED_SOURCE,
            encoding="utf-8",
        )


def _run_pytest(root: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    assert root.resolve() != _REPOSITORY_ROOT.resolve()

    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_CURRENT_TEST", None)

    basetemp = root.parent / f"{root.name}_pytest_basetemp"

    return subprocess.run(
        [
            sys.executable,
            "-B",
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
        check=False,
    )


def _side_effect_fired(root: Path) -> bool:
    return (root / _SIDE_EFFECT_MARKER).exists()


def _archive_side_effect_fired(root: Path) -> bool:
    return (root / _ARCHIVE_SIDE_EFFECT_MARKER).exists()


def _collected_node_ids(output: str) -> frozenset[str]:
    return frozenset(
        line.strip()
        for line in output.splitlines()
        if "::" in line and not line.lstrip().startswith("<")
    )


def _load_tests_conftest():
    specification = importlib.util.spec_from_file_location(
        "fortress_collection_tests_conftest_probe",
        _REAL_TESTS_CONFTEST,
    )
    assert specification is not None
    assert specification.loader is not None

    tests_conftest = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(tests_conftest)
    return tests_conftest


def test_real_tests_conftest_is_present() -> None:
    """The mechanism under test must actually be shipped."""

    assert _REAL_TESTS_CONFTEST.is_file()

    source = _REAL_TESTS_CONFTEST.read_text(encoding="utf-8")

    assert "def pytest_ignore_collect(" in source


def test_real_pytest_configuration_selects_importlib_mode() -> None:
    """F06B owns canonical pytest import semantics in one configuration."""

    parser = configparser.ConfigParser()
    parser.read(_REAL_PYTEST_INI, encoding="utf-8")

    assert "--import-mode=importlib" in parser["pytest"]["addopts"].split()


def test_supported_collection_invocations_share_canonical_node_ids(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F2, F3, F06B: supported collection shapes are structurally equal."""

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    collected_by_invocation: dict[str, frozenset[str]] = {}
    for label, arguments in (
        ("bare", []),
        ("tests-directory", ["tests/"]),
        ("repository-root", ["."]),
    ):
        result = _run_pytest(tmp_path, [*arguments, "--collect-only", "-q"])

        assert result.returncode == 0, result.stdout + result.stderr
        assert not _side_effect_fired(
            tmp_path
        ), f"{label}: the flat legacy module body executed"
        assert not _archive_side_effect_fired(
            tmp_path
        ), f"{label}: an archived module body executed"
        assert "legacy_side_effect_test" not in result.stdout
        assert ".py.legacy" not in result.stdout
        collected_by_invocation[label] = _collected_node_ids(result.stdout)

    expected = collected_by_invocation["bare"]
    assert expected
    assert any("test_canonical_probe_runs" in node_id for node_id in expected)
    assert any(
        "test_importlib_mode_preserves_application_package_identity" in node_id
        for node_id in expected
    )
    assert collected_by_invocation == {
        "bare": expected,
        "tests-directory": expected,
        "repository-root": expected,
    }


def test_importlib_collection_preserves_application_package_identity(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F1, A2, F06B: collision remediation preserves canonical imports."""

    _build_synthetic_tree(tmp_path, include_testpaths=True)

    result = _run_pytest(tmp_path, ["-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout
    assert not _side_effect_fired(tmp_path)
    assert not _archive_side_effect_fired(tmp_path)


def test_containment_does_not_depend_on_testpaths(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """F6: the boundary holds with no testpaths configured at all."""

    _build_synthetic_tree(tmp_path, include_testpaths=False)

    result = _run_pytest(tmp_path, ["tests/", "--collect-only", "-q"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert not _side_effect_fired(tmp_path)
    assert not _archive_side_effect_fired(tmp_path)
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

    This is the evidence that an ignore-based pytest.ini change would not
    help. FORTRESS-06B's import-mode setting addresses package identity and
    does not change this explicit-path limitation.
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
    assert not _archive_side_effect_fired(tmp_path)
    assert "passed" in result.stdout


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

    tests_conftest = _load_tests_conftest()

    tests_root = _REPOSITORY_ROOT / "tests"

    assert tests_conftest.is_excluded_legacy_module(tests_root / "goal_tracker_test.py")
    assert tests_conftest.is_excluded_legacy_module(tests_root / "test_runner.py")
    assert not tests_conftest.is_excluded_legacy_module(tests_root / "__init__.py")
    assert not tests_conftest.is_excluded_legacy_module(tests_root / "conftest.py")
    assert not tests_conftest.is_excluded_legacy_module(
        tests_root / "tests" / "platform" / "test_runtime_paths.py"
    )


def test_every_flat_pytest_shaped_script_is_classified(
    pytestconfig: pytest.Config,
) -> None:
    """The shipped classifier and pytest filename patterns cannot drift."""

    tests_conftest = _load_tests_conftest()
    tests_root = _REPOSITORY_ROOT / "tests"
    patterns = tuple(pytestconfig.getini("python_files"))
    direct_python_files = tuple(tests_root.glob("*.py"))

    pytest_shaped = {
        path
        for path in direct_python_files
        if any(fnmatch.fnmatchcase(path.name, pattern) for pattern in patterns)
    }
    classified = {
        path
        for path in direct_python_files
        if tests_conftest.is_excluded_legacy_module(path)
    }

    assert pytest_shaped
    assert classified == pytest_shaped


def test_root_test_shaped_scripts_are_non_python_archives() -> None:
    """F06B archives exactly two root artifacts without importable code."""

    assert not (_REPOSITORY_ROOT / "phase14_integration_test.py").exists()
    assert not (_REPOSITORY_ROOT / "test_logger.py").exists()
    assert _ARCHIVE_TESTS_ROOT.is_dir()
    assert not (_ARCHIVE_TESTS_ROOT.parent / "__init__.py").exists()
    assert not (_ARCHIVE_TESTS_ROOT / "__init__.py").exists()

    archived_files = {
        path.name for path in _ARCHIVE_TESTS_ROOT.iterdir() if path.is_file()
    }
    assert archived_files == _ARCHIVED_ARTIFACT_NAMES

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    for archived_name in archived_files:
        assert not archived_name.endswith(import_suffixes)

    for former_module_name in _FORMER_ROOT_MODULE_NAMES:
        assert importlib.util.find_spec(former_module_name) is None
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_module_name,
                [str(_ARCHIVE_TESTS_ROOT)],
            )
            is None
        )


_F06D1_QUARANTINED_PATHS = (
    "tests/tests/ai/test_ai_config.py",
    "tests/tests/ai/test_ai_provider_interface.py",
    "tests/tests/ai/test_ai_provider_manager.py",
    "tests/tests/ai/test_ai_provider_models.py",
    "tests/tests/ai/test_llm_router.py",
    "tests/tests/ai/test_prompt_engine.py",
    "tests/tests/ai/test_prompt_models.py",
    "tests/tests/core/test_kernel.py",
)

_F06D1_ARCHIVED_RELPATHS = (
    "legacy_quarantine/tests/ai/test_ai_config.py.legacy",
    "legacy_quarantine/tests/ai/test_ai_provider_interface.py.legacy",
    "legacy_quarantine/tests/ai/test_ai_provider_manager.py.legacy",
    "legacy_quarantine/tests/ai/test_ai_provider_models.py.legacy",
    "legacy_quarantine/tests/ai/test_llm_router.py.legacy",
    "legacy_quarantine/tests/ai/test_prompt_engine.py.legacy",
    "legacy_quarantine/tests/ai/test_prompt_models.py.legacy",
    "legacy_quarantine/tests/core/test_kernel.py.legacy",
)


def test_f06d1_quarantined_tests_are_non_python_archives() -> None:
    """F06D1 archives exactly 8 duplicate AI/Core tests as non-Python legacy files."""

    for former_path in _F06D1_QUARANTINED_PATHS:
        assert not (
            _REPOSITORY_ROOT / former_path
        ).exists(), f"Quarantined path {former_path} must not exist"

    import_suffixes = tuple(importlib.machinery.all_suffixes())

    for archive_relpath in _F06D1_ARCHIVED_RELPATHS:
        archive_path = _REPOSITORY_ROOT / archive_relpath
        assert archive_path.is_file(), f"Archive file {archive_relpath} must exist"
        assert not archive_path.name.endswith(
            import_suffixes
        ), f"{archive_relpath} must not end with a Python suffix"
        assert archive_path.name.endswith(".py.legacy")

    # Verify no __init__.py exists anywhere under legacy_quarantine
    legacy_quarantine_root = _REPOSITORY_ROOT / "legacy_quarantine"
    assert legacy_quarantine_root.is_dir()
    for directory in legacy_quarantine_root.rglob("*"):
        if directory.is_dir():
            assert not (
                directory / "__init__.py"
            ).exists(), f"No __init__.py allowed in {directory}"


_F06D2A_FILESYSTEM_TOOL_STEMS = (
    "test_copy_file_tool",
    "test_delete_file_tool",
    "test_move_file_tool",
    "test_read_file_tool",
    "test_rename_file_tool",
    "test_search_file_tool",
    "test_write_file_tool",
)

_F06D2A_ARCHIVE_ROOT = _ARCHIVE_TESTS_ROOT / "tools" / "filesystem"

_FORBIDDEN_TEST_IMPORT_ROOTS = frozenset(
    {
        "brain",
        "core",
        "executive_brain",
        "kernel",
        "legacy_quarantine",
        "memory",
    }
)


def _imported_top_level_roots(source_path: Path) -> frozenset[str]:
    """Return the statically imported top-level module names of a file."""

    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    roots: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])

    return frozenset(roots)


def test_f06d2a_filesystem_tool_archives_are_non_python() -> None:
    """F06D2A preserves the 7 legacy filesystem tests outside execution."""

    assert _F06D2A_ARCHIVE_ROOT.is_dir()

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    archived_names = {
        path.name for path in _F06D2A_ARCHIVE_ROOT.iterdir() if path.is_file()
    }

    assert archived_names == {
        f"{stem}.py.legacy" for stem in _F06D2A_FILESYSTEM_TOOL_STEMS
    }

    for archived_name in sorted(archived_names):
        archive_path = _F06D2A_ARCHIVE_ROOT / archived_name

        assert not archived_name.endswith(import_suffixes)
        assert "executive_brain" in archive_path.read_text(encoding="utf-8")

    for directory in (_F06D2A_ARCHIVE_ROOT, _F06D2A_ARCHIVE_ROOT.parent):
        assert not (directory / "__init__.py").exists()

    for stem in _F06D2A_FILESYSTEM_TOOL_STEMS:
        assert (
            importlib.machinery.PathFinder.find_spec(
                stem,
                [str(_F06D2A_ARCHIVE_ROOT)],
            )
            is None
        )


def test_f06d2a_configured_filesystem_tests_import_only_canonical_tools() -> None:
    """F06D2A's configured replacements depend on ``jaos.tools`` alone."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests" / "tools"

    for stem in _F06D2A_FILESYSTEM_TOOL_STEMS:
        configured_path = configured_root / f"{stem}.py"

        assert configured_path.is_file()

        roots = _imported_top_level_roots(configured_path)

        assert "jaos" in roots
        assert not roots & _FORBIDDEN_TEST_IMPORT_ROOTS, (
            f"{configured_path.name} must not import legacy roots: "
            f"{sorted(roots & _FORBIDDEN_TEST_IMPORT_ROOTS)}"
        )


_F06D2B_TOOL_PLATFORM_STEMS = (
    "test_tool_interface",
    "test_tool_manager",
    "test_tool_models",
    "test_tool_registry",
)

_F06D2B_ARCHIVE_ROOT = _ARCHIVE_TESTS_ROOT / "tools" / "core"


def test_f06d2b_tool_platform_archives_are_non_python() -> None:
    """F06D2B preserves the 4 legacy Tool Platform tests outside execution."""

    assert _F06D2B_ARCHIVE_ROOT.is_dir()

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    archived_names = {
        path.name for path in _F06D2B_ARCHIVE_ROOT.iterdir() if path.is_file()
    }

    assert archived_names == {
        f"{stem}.py.legacy" for stem in _F06D2B_TOOL_PLATFORM_STEMS
    }

    for archived_name in sorted(archived_names):
        archive_path = _F06D2B_ARCHIVE_ROOT / archived_name

        assert not archived_name.endswith(import_suffixes)
        assert "executive_brain.tools.core" in archive_path.read_text(
            encoding="utf-8"
        )

    assert not (_F06D2B_ARCHIVE_ROOT / "__init__.py").exists()

    for stem in _F06D2B_TOOL_PLATFORM_STEMS:
        assert (
            importlib.machinery.PathFinder.find_spec(
                stem,
                [str(_F06D2B_ARCHIVE_ROOT)],
            )
            is None
        )


def test_f06d2b_configured_tool_platform_tests_import_only_canonical_tools() -> None:
    """F06D2B's configured replacements depend on ``jaos.tools`` alone."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests" / "tools"

    for stem in _F06D2B_TOOL_PLATFORM_STEMS:
        configured_path = configured_root / f"{stem}.py"

        assert configured_path.is_file()

        roots = _imported_top_level_roots(configured_path)

        assert "jaos" in roots
        assert not roots & _FORBIDDEN_TEST_IMPORT_ROOTS, (
            f"{configured_path.name} must not import legacy roots: "
            f"{sorted(roots & _FORBIDDEN_TEST_IMPORT_ROOTS)}"
        )


_F06D2E_REMAINING_LEGACY_TOOL_TEST_STEMS = (
    "test_browser_automation_tool",
    "test_build_tool",
    "test_clipboard_tool",
    "test_close_application_tool",
    "test_cookies_tool",
    "test_debug_tool",
    "test_downloads_tool",
    "test_git_tool",
    "test_launch_application_tool",
    "test_notification_tool",
    "test_process_manager_tool",
    "test_project_tool",
    "test_run_tool",
    "test_services_tool",
    "test_tabs_tool",
    "test_web_search_tool",
)


def _imports_legacy_tool_platform(source_path: Path) -> bool:
    """Return whether a file statically imports ``executive_brain.tools.core``."""

    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules = (node.module,)
        elif isinstance(node, ast.Import):
            modules = tuple(alias.name for alias in node.names)
        else:
            continue

        if any(
            module.startswith("executive_brain.tools.core") for module in modules
        ):
            return True

    return False


def test_f06d2b_migrated_paths_no_longer_depend_on_the_legacy_tool_platform() -> None:
    """The four adjudicated paths carry no ``executive_brain.tools.core`` import.

    The remaining legacy Tool Platform importers are the prototype browser,
    Windows, and development per-tool configured tests owned by FORTRESS-06D2E.
    Pinning that inventory keeps the residue visible and prevents it from
    silently growing while F06D2E is unstarted.
    """

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"

    offenders = sorted(
        configured_path.relative_to(_REPOSITORY_ROOT).as_posix()
        for configured_path in configured_root.rglob("*.py")
        if "__pycache__" not in configured_path.parts
        and _imports_legacy_tool_platform(configured_path)
    )

    for stem in _F06D2B_TOOL_PLATFORM_STEMS:
        migrated_path = (
            (configured_root / "tools" / f"{stem}.py")
            .relative_to(_REPOSITORY_ROOT)
            .as_posix()
        )

        assert migrated_path not in offenders

    assert offenders == sorted(
        f"tests/tests/tools/{stem}.py"
        for stem in _F06D2E_REMAINING_LEGACY_TOOL_TEST_STEMS
    )
