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
import hashlib
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


_F06D2E_PROTOTYPE_TOOL_TEST_STEMS = (
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

    FORTRESS-06D2E subsequently retired the prototype browser, Windows, and
    development residue, so no configured test may import that shadow core.
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

    assert len(_F06D2E_PROTOTYPE_TOOL_TEST_STEMS) == 16
    assert offenders == []


_F06D2C_ARCHIVE_PAIRS = (
    (
        "tests/tests/brain/test_executive_brain.py",
        (
            "legacy_quarantine/tests/executive/brain/"
            "test_executive_brain.py.legacy"
        ),
    ),
    (
        "tests/tests/integration/test_executive_pipeline.py",
        (
            "legacy_quarantine/tests/executive/pipeline/"
            "test_executive_pipeline.py.legacy"
        ),
    ),
    (
        "tests/tests/integration/test_executive_pipeline_v2.py",
        (
            "legacy_quarantine/tests/executive/pipeline/"
            "test_executive_pipeline_v2.py.legacy"
        ),
    ),
    (
        "tests/tests/integration/test_executive_runtime.py",
        (
            "legacy_quarantine/tests/executive/runtime/"
            "test_executive_runtime.py.legacy"
        ),
    ),
)
_F06D2C_CANONICAL_TEST_PATH = (
    _REPOSITORY_ROOT
    / "tests"
    / "tests"
    / "executive"
    / "test_canonical_executive_controller.py"
)
_F06D2C_ADJACENT_MEMORY_RUNTIME_PATH = (
    _REPOSITORY_ROOT
    / "tests"
    / "tests"
    / "integration"
    / "test_memory_runtime_integration.py"
)


def test_f06d2c_executive_archives_are_non_python_and_non_collectable(
    pytestconfig: pytest.Config,
) -> None:
    """F06D2C preserves exactly four Executive test payloads outside execution."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))

    for former_relpath, archive_relpath in _F06D2C_ARCHIVE_PAIRS:
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )
        assert "executive_brain" in archive_path.read_text(encoding="utf-8")
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )
        assert not (archive_path.parent / "__init__.py").exists()


def test_f06d2c_canonical_executive_test_uses_only_canonical_authorities() -> None:
    """The D2C replacement reaches canonical JAOS and no legacy import root."""

    assert _F06D2C_CANONICAL_TEST_PATH.is_file()

    roots = _imported_top_level_roots(_F06D2C_CANONICAL_TEST_PATH)

    assert roots == frozenset({"jaos", "pathlib", "pytest", "unittest"})
    assert not roots & _FORBIDDEN_TEST_IMPORT_ROOTS


def test_f06d2c_retirement_remains_contained_after_memory_retirement() -> None:
    """D2C's paths stay retired after ADR-0013 retires adjacent Memory."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
        and "executive_brain" in _imported_top_level_roots(path)
    }

    assert not {
        former_relpath for former_relpath, _archive in _F06D2C_ARCHIVE_PAIRS
    } & executive_importers
    assert not _F06D2C_ADJACENT_MEMORY_RUNTIME_PATH.exists()
    assert (
        "tests/tests/integration/test_memory_runtime_integration.py"
        not in executive_importers
    )


_F06D2D_ARCHIVE_RECORDS = (
    (
        "tests/tests/manager_layer/test_decision_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_decision_manager.py.legacy"
        ),
        "ba1b17667115e75129ed8b5c27a24a433b96d71991ddcd7ea6c763588cef4e5a",
    ),
    (
        "tests/tests/manager_layer/test_execution_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_execution_manager.py.legacy"
        ),
        "229639f71adbcb519c62fc1fee8c7f4b708169d469115f61fdd45971c1d88997",
    ),
    (
        "tests/tests/manager_layer/test_mission_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_mission_manager.py.legacy"
        ),
        "60b4d90e80ca2750109fcfae23e1c42b960302ee0fb6dd9eeccc9640af193b88",
    ),
    (
        "tests/tests/manager_layer/test_planning_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_planning_manager.py.legacy"
        ),
        "a56b590b241de2aec25b1bfa3c6c1f513ccd91e3d134cd963a5d0054adbea516",
    ),
    (
        "tests/tests/manager_layer/test_registry_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_registry_manager.py.legacy"
        ),
        "473bd4914180c0be406bb69a319183c5759149ec75b1cf8614e44390419eadcd",
    ),
    (
        "tests/tests/manager_layer/test_result_manager.py",
        (
            "legacy_quarantine/tests/executive/managers/"
            "test_result_manager.py.legacy"
        ),
        "15c84c43aadbecc91a0e8f82cd8e300510c9ad5c7909b5b973f06e16ec52e628",
    ),
    (
        "tests/tests/registry_layer/test_execution_plan_registry.py",
        (
            "legacy_quarantine/tests/executive/registries/"
            "test_execution_plan_registry.py.legacy"
        ),
        "6174dd08b9ad419684b4994f0bc2ebe2053892cad804959bd8916efbb647a111",
    ),
    (
        "tests/tests/registry_layer/test_mission_registry.py",
        (
            "legacy_quarantine/tests/executive/registries/"
            "test_mission_registry.py.legacy"
        ),
        "e91aadb273f1175d424ad4e4a5a70e4c39aebfc1256931bba4677a2803c6b0e6",
    ),
    (
        "tests/tests/registry_layer/test_result_registry.py",
        (
            "legacy_quarantine/tests/executive/registries/"
            "test_result_registry.py.legacy"
        ),
        "ae977136dcd578136ba074d9bd741d6c69f1fbd710e103aa382508be0440ea7e",
    ),
)

_F06D_MEMORY_RETIRED_IMPORTERS = frozenset(
    {
        "tests/tests/integration/test_memory_runtime_integration.py",
        "tests/tests/memory/test_memory_manager.py",
        "tests/tests/memory/test_memory_registry.py",
        "tests/tests/memory/test_working_memory.py",
    }
)

_F06D_PROVIDER_RETIRED_IMPORTERS = frozenset(
    {
        "tests/tests/ai/test_ollama_provider.py",
        "tests/tests/ai/test_openai_provider.py",
    }
)


def test_f06d2d_manager_registry_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """D2D archives nine byte-identical payloads outside Python collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))

    for former_relpath, archive_relpath, expected_sha256 in _F06D2D_ARCHIVE_RECORDS:
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )
        assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == expected_sha256
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    legacy_quarantine_root = _REPOSITORY_ROOT / "legacy_quarantine"
    assert not tuple(legacy_quarantine_root.rglob("__init__.py"))


def test_f06d2d_deferred_provider_inventory_is_now_retired() -> None:
    """ADR-0014 retires the provider residue that D2D originally deferred."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
        and "executive_brain" in _imported_top_level_roots(path)
    }
    retired_tool_importers = {
        f"tests/tests/tools/{stem}.py"
        for stem in _F06D2E_PROTOTYPE_TOOL_TEST_STEMS
    }

    assert not retired_tool_importers & executive_importers
    assert not _F06D_MEMORY_RETIRED_IMPORTERS & configured_paths
    assert not _F06D_PROVIDER_RETIRED_IMPORTERS & configured_paths
    assert executive_importers == set()
    assert len(retired_tool_importers) == 16
    assert len(_F06D_MEMORY_RETIRED_IMPORTERS) == 4
    assert len(_F06D_PROVIDER_RETIRED_IMPORTERS) == 2


_F06D2E_ARCHIVE_RECORDS = (
    (
        "tests/tests/tools/test_browser_automation_tool.py",
        (
            "legacy_quarantine/tests/tools/browser/"
            "test_browser_automation_tool.py.legacy"
        ),
        "e68acf8fc99a0f01549269ab1fdedaf1dfb23b842312b49da0d8ab619b2c44b8",
    ),
    (
        "tests/tests/tools/test_cookies_tool.py",
        "legacy_quarantine/tests/tools/browser/test_cookies_tool.py.legacy",
        "76cf2a665f39bb9a61081c4e26b90903127a9fe85b528653b6248a511162e5e8",
    ),
    (
        "tests/tests/tools/test_downloads_tool.py",
        "legacy_quarantine/tests/tools/browser/test_downloads_tool.py.legacy",
        "0f996ef7d135b2dbd56560b206e0ef693551a54617a65ea1b73919dc42a2a8d6",
    ),
    (
        "tests/tests/tools/test_tabs_tool.py",
        "legacy_quarantine/tests/tools/browser/test_tabs_tool.py.legacy",
        "bee2d7bffb76e60522ed7bf1cc32128609715165bbd1ca21068988fb8b94b9c6",
    ),
    (
        "tests/tests/tools/test_web_search_tool.py",
        "legacy_quarantine/tests/tools/browser/test_web_search_tool.py.legacy",
        "29411462583b8f8907601a929ecf83baf0b8f54b753d99d8cbee72a6f5419485",
    ),
    (
        "tests/tests/tools/test_clipboard_tool.py",
        "legacy_quarantine/tests/tools/windows/test_clipboard_tool.py.legacy",
        "92665f98366b589962fd70f02f62e7694013b9efc43c617444f2e724b81cc745",
    ),
    (
        "tests/tests/tools/test_close_application_tool.py",
        (
            "legacy_quarantine/tests/tools/windows/"
            "test_close_application_tool.py.legacy"
        ),
        "dd385440ab3e943c6b1fa7e4c29668ca5b40f4e8e8738d7314ff81240b2546d1",
    ),
    (
        "tests/tests/tools/test_launch_application_tool.py",
        (
            "legacy_quarantine/tests/tools/windows/"
            "test_launch_application_tool.py.legacy"
        ),
        "a6e234a6a698044c9615cb6e8210cc418c6375f7813ed0c14776f0e5f25abf82",
    ),
    (
        "tests/tests/tools/test_notification_tool.py",
        "legacy_quarantine/tests/tools/windows/test_notification_tool.py.legacy",
        "0bb6181c2e446d8c4821570d237bcbfb4e3e17538dc67047ac64966a3a829685",
    ),
    (
        "tests/tests/tools/test_process_manager_tool.py",
        (
            "legacy_quarantine/tests/tools/windows/"
            "test_process_manager_tool.py.legacy"
        ),
        "77d9caf19db420ed994f1e4f9e076c8b5959a2ac436e49afbc41c86a498b9828",
    ),
    (
        "tests/tests/tools/test_services_tool.py",
        "legacy_quarantine/tests/tools/windows/test_services_tool.py.legacy",
        "1fad7e0fb3b6c54248062d2c6774638b7648b0fe639439cc2205661d6f1fc5f2",
    ),
    (
        "tests/tests/tools/test_build_tool.py",
        "legacy_quarantine/tests/tools/development/test_build_tool.py.legacy",
        "1c0ae4f4cfd506f48d24a33401713a06c83c32a30b4d3a5edddc9aebf6bfbf5f",
    ),
    (
        "tests/tests/tools/test_debug_tool.py",
        "legacy_quarantine/tests/tools/development/test_debug_tool.py.legacy",
        "43a44695d3b135702c751fa53f88c015f6de8c888d1b65a35f0932ef3af06318",
    ),
    (
        "tests/tests/tools/test_git_tool.py",
        "legacy_quarantine/tests/tools/development/test_git_tool.py.legacy",
        "76b5c4344074b62cc9a827514ae82c08af2740fc8c4a02405c30619a0627e74f",
    ),
    (
        "tests/tests/tools/test_project_tool.py",
        "legacy_quarantine/tests/tools/development/test_project_tool.py.legacy",
        "300396f4067fde5b6ad0c321ab9da75a69af1e36c784a11513c0bdeba616690f",
    ),
    (
        "tests/tests/tools/test_run_tool.py",
        "legacy_quarantine/tests/tools/development/test_run_tool.py.legacy",
        "168998f989ae5b9ebf36fb2fc5421bbef5752c01e3f4123348189fbff0fdc97a",
    ),
)

_F06D2E_PRODUCTION_PROTOTYPE_PATHS = (
    "executive_brain/tools/browser/browser_automation_tool.py",
    "executive_brain/tools/browser/cookies_tool.py",
    "executive_brain/tools/browser/downloads_tool.py",
    "executive_brain/tools/browser/tabs_tool.py",
    "executive_brain/tools/browser/web_search_tool.py",
    "executive_brain/tools/windows/clipboard_tool.py",
    "executive_brain/tools/windows/close_application_tool.py",
    "executive_brain/tools/windows/launch_application_tool.py",
    "executive_brain/tools/windows/notification_tool.py",
    "executive_brain/tools/windows/process_manager_tool.py",
    "executive_brain/tools/windows/services_tool.py",
    "executive_brain/tools/development/vscode/build_tool.py",
    "executive_brain/tools/development/vscode/debug_tool.py",
    "executive_brain/tools/development/vscode/git_tool.py",
    "executive_brain/tools/development/vscode/project_tool.py",
    "executive_brain/tools/development/vscode/run_tool.py",
)

_F06D2E_LEGACY_FACING_IMPORT_ROOTS = frozenset(
    {
        "communication",
        "core",
        "dashboard",
        "development",
        "engineering",
        "executive_brain",
        "infrastructure",
        "kernel",
        "knowledge",
        "pc_control",
        "security",
        "system_services",
        "workflow",
    }
)

_F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS = frozenset(
    {
        "tests/tests/platform/test_config_containment.py",
    }
)


def test_f06d2e_prototype_tool_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """D2E preserves 16 exact payloads outside Python and pytest collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))

    assert len(_F06D2E_ARCHIVE_RECORDS) == 16
    assert sum("/browser/" in record[1] for record in _F06D2E_ARCHIVE_RECORDS) == 5
    assert sum("/windows/" in record[1] for record in _F06D2E_ARCHIVE_RECORDS) == 6
    assert sum(
        "/development/" in record[1] for record in _F06D2E_ARCHIVE_RECORDS
    ) == 5

    for former_relpath, archive_relpath, expected_sha256 in _F06D2E_ARCHIVE_RECORDS:
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )
        assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == expected_sha256
        assert "executive_brain.tools.core" in archive_path.read_text(
            encoding="utf-8"
        )
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    legacy_quarantine_root = _REPOSITORY_ROOT / "legacy_quarantine"
    assert not tuple(legacy_quarantine_root.rglob("__init__.py"))


def test_f06d2e_retires_exact_prototype_inventory_and_preserves_residue() -> None:
    """D2E archives stay contained after later provider retirement."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = tuple(
        path
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    retired_paths = {
        former_relpath for former_relpath, _archive, _sha in _F06D2E_ARCHIVE_RECORDS
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if "executive_brain" in _imported_top_level_roots(path)
    }
    legacy_core_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imports_legacy_tool_platform(path)
    }
    legacy_facing_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }

    assert not retired_paths & {
        path.relative_to(_REPOSITORY_ROOT).as_posix() for path in configured_paths
    }
    assert legacy_core_importers == set()
    assert executive_importers == set()
    assert legacy_facing_paths == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 1

    assert len(_F06D2E_PRODUCTION_PROTOTYPE_PATHS) == 16
    for prototype_relpath in _F06D2E_PRODUCTION_PROTOTYPE_PATHS:
        assert (_REPOSITORY_ROOT / prototype_relpath).is_file()


_F06D_MEMORY_ARCHIVE_RECORDS = (
    (
        "tests/tests/integration/test_memory_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_memory_runtime_integration.py.legacy"
        ),
        "83bdf8e9cfd5b01fc9b487b4a1d9928fd30e14128beded4a226a97b7f30b9024",
        4,
    ),
    (
        "tests/tests/memory/test_memory_manager.py",
        "legacy_quarantine/tests/memory/test_memory_manager.py.legacy",
        "1c888f4d7c9950a2f1090fe06d8dff3de77ea9d7bdbc02c49a73fa5b5e90b094",
        9,
    ),
    (
        "tests/tests/memory/test_memory_registry.py",
        "legacy_quarantine/tests/memory/test_memory_registry.py.legacy",
        "b2503c77d160f01dd9c6a3b284086862cb27da297f52b78f5a39abdd0013378e",
        7,
    ),
    (
        "tests/tests/memory/test_working_memory.py",
        "legacy_quarantine/tests/memory/test_working_memory.py.legacy",
        "a09fa6bb85e7716d1622a2d75275963ba0081ac8ba36bee05bbcba76e35bb353",
        10,
    ),
)

_F06D_MEMORY_PRODUCTION_PATHS = (
    "executive_brain/memory/memory_manager.py",
    "executive_brain/memory/memory_registry.py",
    "executive_brain/memory/working_memory.py",
)

_F06D_MEMORY_RAA009_PATHS = (
    "jaos/intelligence/context/memory_context_source.py",
    "jaos/memory/storage/memory_search_engine.py",
)


def _imports_legacy_memory(source_path: Path) -> bool:
    """Return whether a file statically imports legacy Executive Memory."""

    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules = (node.module,)
        elif isinstance(node, ast.Import):
            modules = tuple(alias.name for alias in node.names)
        else:
            continue

        if any(module.startswith("executive_brain.memory") for module in modules):
            return True

    return False


def test_f06d_memory_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """ADR-0013 archives four exact payloads outside Python collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    source_test_total = 0

    assert len(_F06D_MEMORY_ARCHIVE_RECORDS) == 4

    for former_relpath, archive_relpath, expected_sha256, test_count in (
        _F06D_MEMORY_ARCHIVE_RECORDS
    ):
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )
        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        source_tree = ast.parse(payload.decode("utf-8"))
        archived_tests = tuple(
            node
            for node in ast.walk(source_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
        assert len(archived_tests) == test_count
        source_test_total += len(archived_tests)
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    assert source_test_total == 30
    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )


def test_f06d_memory_retirement_remains_contained_after_provider_retirement() -> None:
    """Memory quarantine stays contained after the provider residue retires."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = tuple(
        path
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    configured_relpaths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if "executive_brain" in _imported_top_level_roots(path)
    }
    memory_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imports_legacy_memory(path)
    }
    legacy_facing_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }

    assert not _F06D_MEMORY_RETIRED_IMPORTERS & configured_relpaths
    assert memory_importers == set()
    assert not _F06D_PROVIDER_RETIRED_IMPORTERS & configured_relpaths
    assert executive_importers == set()
    assert legacy_facing_paths == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 1

    for production_relpath in _F06D_MEMORY_PRODUCTION_PATHS:
        assert (_REPOSITORY_ROOT / production_relpath).is_file()
    for raa009_relpath in _F06D_MEMORY_RAA009_PATHS:
        assert (_REPOSITORY_ROOT / raa009_relpath).is_file()


_F06D_PROVIDER_ARCHIVE_RECORDS = (
    (
        "tests/tests/ai/test_ollama_provider.py",
        "legacy_quarantine/tests/ai/test_ollama_provider.py.legacy",
        "4b25c507f2bb886479514e324bfd4df0d366f98db2898e87ff7070dbd1153c30",
        9,
    ),
    (
        "tests/tests/ai/test_openai_provider.py",
        "legacy_quarantine/tests/ai/test_openai_provider.py.legacy",
        "cfc6d61aa8886c6b8a07d28c8108ca2998103bcf7129212a05771c9ee04192e6",
        11,
    ),
)

_F06D_PROVIDER_CANONICAL_TEST_PATH = (
    _REPOSITORY_ROOT
    / "tests"
    / "tests"
    / "ai"
    / "test_canonical_provider_contract.py"
)

_F06D_PROVIDER_PRODUCTION_PATHS = (
    "executive_brain/ai/providers/ollama_provider.py",
    "executive_brain/ai/providers/openai_provider.py",
)


def test_f06d_provider_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """ADR-0014 preserves both exact provider payloads outside collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    source_test_total = 0

    assert len(_F06D_PROVIDER_ARCHIVE_RECORDS) == 2

    for former_relpath, archive_relpath, expected_sha256, test_count in (
        _F06D_PROVIDER_ARCHIVE_RECORDS
    ):
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )

        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        assert "executive_brain.ai.providers" in payload.decode("utf-8")

        source_tree = ast.parse(payload.decode("utf-8"))
        archived_tests = tuple(
            node
            for node in ast.walk(source_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
        assert len(archived_tests) == test_count
        source_test_total += len(archived_tests)
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    assert source_test_total == 20
    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )


def test_f06d_provider_retirement_preserves_canonical_and_legacy_boundaries() -> None:
    """Provider retirement leaves canonical tests and the exact F06 residue."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = tuple(
        path
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    configured_relpaths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if "executive_brain" in _imported_top_level_roots(path)
    }
    legacy_facing_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }

    assert _F06D_PROVIDER_CANONICAL_TEST_PATH.is_file()
    assert _imported_top_level_roots(_F06D_PROVIDER_CANONICAL_TEST_PATH) == {
        "jaos",
        "pytest",
    }
    assert not _F06D_PROVIDER_RETIRED_IMPORTERS & configured_relpaths
    assert executive_importers == set()
    assert legacy_facing_paths == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 1

    for production_relpath in _F06D_PROVIDER_PRODUCTION_PATHS:
        assert (_REPOSITORY_ROOT / production_relpath).is_file()


_F06D_SATELLITE_ARCHIVE_RECORDS = (
    (
        "tests/tests/integration/test_communication_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_communication_runtime_integration.py.legacy"
        ),
        "64a85ec44c7469fd9b1e5b8334668d67e6e736a4ed8b9c077073b676c033c8e3",
        3,
    ),
    (
        "tests/tests/integration/test_dashboard_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_dashboard_runtime_integration.py.legacy"
        ),
        "7d098bc62d40594125a3ba631187438685e25a9b7842d30986ed21ae98b12428",
        3,
    ),
    (
        "tests/tests/integration/test_development_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_development_runtime_integration.py.legacy"
        ),
        "3e269159210a0a0c17592bb59ffff53cfcec53cb5fd4a2c60fd2f42ec9116888",
        3,
    ),
    (
        "tests/tests/integration/test_engineering_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_engineering_runtime_integration.py.legacy"
        ),
        "4fcef4fcca5c604f613f229b81916aea7fa8a5d8e96dc362ee83475c76eb62fd",
        3,
    ),
    (
        "tests/tests/integration/test_infrastructure_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_infrastructure_runtime_integration.py.legacy"
        ),
        "773d975c2155aa093a3f16cf8f6748b3870016e3ac401704f6ffd40f6361b04a",
        3,
    ),
    (
        "tests/tests/integration/test_knowledge_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_knowledge_runtime_integration.py.legacy"
        ),
        "b4551ead376823afdfee721322f5015326adab87be229d7971621a8d49f4c2ef",
        3,
    ),
    (
        "tests/tests/integration/test_pc_control_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_pc_control_runtime_integration.py.legacy"
        ),
        "d97e91ef336b7fc6086ce97d03bc5e102b3d01b6cee2acadd37d57bbd79a881c",
        3,
    ),
    (
        "tests/tests/integration/test_security_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_security_runtime_integration.py.legacy"
        ),
        "32e56102ec63eced4534ab17f914c6d71a1ed9132e5430c37d5057b1a25e64d7",
        3,
    ),
    (
        "tests/tests/integration/test_system_services_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_system_services_runtime_integration.py.legacy"
        ),
        "1db3d498db9633d21d809ae5bfa7d9f58f1c14866fcd1f98f660eb53efdcf097",
        3,
    ),
    (
        "tests/tests/integration/test_workflow_runtime_integration.py",
        (
            "legacy_quarantine/tests/integration/"
            "test_workflow_runtime_integration.py.legacy"
        ),
        "6bbfc848eeb30af9788bc2f3ad0897810dec8f4c6ced072227f3ac8e808bf83b",
        3,
    ),
)

_F06D_SATELLITE_PRODUCTION_PATHS = (
    "workflow/workflow_engine.py",
)

_F06D_RETAINED_CORE_KERNEL_CONFIG_PATHS = (
    "core/config_manager.py",
    "core/engine.py",
    "kernel/jaos_kernel.py",
    "main.py",
)


def test_f06d_satellite_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """Ten exact satellite payloads remain outside Python and pytest collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    source_test_total = 0

    assert len(_F06D_SATELLITE_ARCHIVE_RECORDS) == 10

    for former_relpath, archive_relpath, expected_sha256, test_count in (
        _F06D_SATELLITE_ARCHIVE_RECORDS
    ):
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )

        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        source_tree = ast.parse(payload.decode("utf-8"))
        archived_tests = tuple(
            node
            for node in ast.walk(source_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
        assert len(archived_tests) == test_count
        source_test_total += len(archived_tests)
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    assert source_test_total == 30
    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )


def test_f06d_satellite_retirement_preserves_exact_residual_boundaries() -> None:
    """Satellite archives stay contained after core/kernel test retirement."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = tuple(
        path
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    configured_relpaths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if "executive_brain" in _imported_top_level_roots(path)
    }
    legacy_facing_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }
    retired_paths = {
        former_relpath
        for former_relpath, _archive, _sha256, _count in (
            _F06D_SATELLITE_ARCHIVE_RECORDS
        )
    }

    assert not retired_paths & configured_relpaths
    assert executive_importers == set()
    assert legacy_facing_paths == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 1

    for production_relpath in _F06D_SATELLITE_PRODUCTION_PATHS:
        assert (_REPOSITORY_ROOT / production_relpath).is_file()
    production_archives = {
        former: (archive, sha256, blob)
        for former, archive, sha256, blob in (
            _F06E_SATELLITE_PRODUCTION_ARCHIVE_RECORDS
            + _F06E_DYNAMIC_SATELLITE_ARCHIVE_RECORDS
            + _F06E_ENGINEERING_ARCHIVE_RECORDS
        )
    }
    for former_relpath in (
        "engineering/platform_health_dashboard.py",
        "development/development_workspace_manager.py",
        "infrastructure/ai_provider_manager.py",
        "pc_control/application_manager.py",
        "dashboard/mission_control.py",
        "knowledge/knowledge_base.py",
        "security/security_monitor.py",
        "system_services/startup_manager.py",
    ):
        archive, sha256, blob = production_archives[former_relpath]
        assert not (_REPOSITORY_ROOT / former_relpath).exists()
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == sha256
        assert _git_blob_id(payload, path=archive) == blob
    for retained_relpath in _F06D_RETAINED_CORE_KERNEL_CONFIG_PATHS:
        assert (_REPOSITORY_ROOT / retained_relpath).is_file()


_F06D_CORE_KERNEL_ARCHIVE_RECORDS = (
    (
        "tests/tests/platform/test_core_runtime_integration.py",
        "legacy_quarantine/tests/platform/test_core_runtime_integration.py.legacy",
        "7cea6699d3842677ba3b78796f385e8f57670ae22208418955d01666bed8bd39",
        3,
    ),
    (
        "tests/tests/platform/test_kernel_runtime_integration.py",
        "legacy_quarantine/tests/platform/test_kernel_runtime_integration.py.legacy",
        "d629bbb6ee27bff0bcb170c04b7e13ec6946a67f05e9ef041a93994f57cea85d",
        3,
    ),
)

_F06D_CONFIG_CONTAINMENT_PATH = (
    _REPOSITORY_ROOT / "tests" / "tests" / "platform" / "test_config_containment.py"
)
_F06D_CONFIG_CONTAINMENT_SHA256 = (
    "d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c"
)
_F06D_CORE_KERNEL_PRODUCTION_PATHS = (
    "core/engine.py",
    "kernel/jaos_kernel.py",
    "main.py",
)


def test_f06d_core_kernel_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """Two exact core/kernel payloads remain outside configured collection."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    source_test_total = 0

    assert len(_F06D_CORE_KERNEL_ARCHIVE_RECORDS) == 2

    for former_relpath, archive_relpath, expected_sha256, test_count in (
        _F06D_CORE_KERNEL_ARCHIVE_RECORDS
    ):
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )

        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        source_tree = ast.parse(payload.decode("utf-8"))
        archived_tests = tuple(
            node
            for node in ast.walk(source_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
        assert len(archived_tests) == test_count
        source_test_total += len(archived_tests)
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    assert source_test_total == 6
    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )


def _assert_config_containment_preserved() -> None:
    config_payload = _F06D_CONFIG_CONTAINMENT_PATH.read_bytes()
    assert hashlib.sha256(config_payload).hexdigest() == (
        _F06D_CONFIG_CONTAINMENT_SHA256
    )
    config_tree = ast.parse(config_payload.decode("utf-8"))
    config_tests = tuple(
        node
        for node in ast.walk(config_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    )
    parametrized_expansion = sum(
        len(decorator.args[1].elts) - 1
        for test_node in config_tests
        for decorator in test_node.decorator_list
        if isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Attribute)
        and decorator.func.attr == "parametrize"
        and len(decorator.args) >= 2
        and isinstance(decorator.args[1], (ast.List, ast.Tuple))
    )
    assert len(config_tests) == 9
    assert len(config_tests) + parametrized_expansion == 11


def test_f06d_core_kernel_retirement_leaves_only_config_containment() -> None:
    """Only the governed config/writer boundary remains legacy-facing."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
    configured_paths = tuple(
        path
        for path in configured_root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    configured_relpaths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
    }
    executive_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if "executive_brain" in _imported_top_level_roots(path)
    }
    legacy_facing_paths = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }
    retired_paths = {
        former_relpath
        for former_relpath, _archive, _sha256, _count in (
            _F06D_CORE_KERNEL_ARCHIVE_RECORDS
        )
    }

    assert not retired_paths & configured_relpaths
    assert executive_importers == set()
    assert legacy_facing_paths == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 1

    _assert_config_containment_preserved()

    for production_relpath in _F06D_CORE_KERNEL_PRODUCTION_PATHS:
        assert (_REPOSITORY_ROOT / production_relpath).is_file()


_F06E_COMMUNICATION_ARCHIVE_RECORDS = (
    (
        "communication/calendar_manager.py",
        (
            "legacy_quarantine/production/communication/"
            "calendar_manager.py.legacy"
        ),
        "de550bf3ddb8ea4c7c9be56e492f54c54dfa5280a7e8ef853def40eea8894911",
        "807089aa2bc86cf92f42ae65fa8ececddc13db98",
    ),
    (
        "communication/communication_hub.py",
        (
            "legacy_quarantine/production/communication/"
            "communication_hub.py.legacy"
        ),
        "d34c4f6b33410c69498493675fef02d59ae88e7bee366c97d6311c0295eca02b",
        "65bb8f303128b6847fa2ac9913af5d627ad82ec1",
    ),
    (
        "communication/contacts_manager.py",
        (
            "legacy_quarantine/production/communication/"
            "contacts_manager.py.legacy"
        ),
        "2f0c86a51200d40513d3827def63c464c8f3fc10d2cce433a761a999932bb565",
        "69f189614e5c5fbf707561752b99fec3fd9a154f",
    ),
    (
        "communication/conversation_manager.py",
        (
            "legacy_quarantine/production/communication/"
            "conversation_manager.py.legacy"
        ),
        "8bace0ec95836012cf3cf7fceb2fae929068ca975c010502a33e51a05cb0e72b",
        "3dacf67cda7110b7b92c8b76e9141a63ee5470c4",
    ),
    (
        "communication/email_manager.py",
        (
            "legacy_quarantine/production/communication/"
            "email_manager.py.legacy"
        ),
        "997d2c4ea5cfb8fd82194d86158a07b5b8d593dcc22cb5f0fec42f595500d08b",
        "824e1eccc45973d45aad7988397e86df211b6dd7",
    ),
    (
        "communication/meeting_assistant.py",
        (
            "legacy_quarantine/production/communication/"
            "meeting_assistant.py.legacy"
        ),
        "e8ff0e6b877b3c4546c4c6810cb418c41b0210b5896956fa60de8608f35bf542",
        "c36d257ebcf8a5b91ca4f4c96b43655581a7789a",
    ),
)
_F06E_COMMUNICATION_EXCLUDED_TEST_IMPORTERS = frozenset(
    {
        "tests/calendar_manager_test.py",
        "tests/communication_hub_test.py",
        "tests/communication_platform_integration_test.py",
        "tests/contacts_manager_test.py",
        "tests/conversation_manager_test.py",
        "tests/email_manager_test.py",
        "tests/meeting_assistant_test.py",
    }
)


def _git_blob_id(payload: bytes, *, path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", f"--path={path}", "--stdin"],
        cwd=_REPOSITORY_ROOT,
        input=payload,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout.decode("ascii").strip()


def _repository_live_python_paths() -> tuple[Path, ...]:
    result = subprocess.run(
        [
            "git", "ls-files", "-z", "--cached", "--others",
            "--exclude-standard", "--", "*.py",
        ],
        cwd=_REPOSITORY_ROOT,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return tuple(
        path
        for relpath in result.stdout.decode("utf-8").split("\0")
        if relpath
        if (path := _REPOSITORY_ROOT / relpath).is_file()
    )


def _literal_dynamic_import_roots(source_path: Path) -> frozenset[str]:
    source_tree = ast.parse(source_path.read_text(encoding="utf-8-sig"))
    roots: set[str] = set()

    for node in ast.walk(source_tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        function_name = None
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        if function_name not in {"import_module", "__import__", "add_import"}:
            continue
        module_argument = node.args[0]
        if isinstance(module_argument, ast.Constant) and isinstance(
            module_argument.value, str
        ):
            roots.add(module_argument.value.partition(".")[0])

    return frozenset(roots)


def test_f06e_communication_production_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """Six exact production payloads remain inert and reversible."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))

    assert len(_F06E_COMMUNICATION_ARCHIVE_RECORDS) == 6

    for former_relpath, archive_relpath, expected_sha256, expected_blob in (
        _F06E_COMMUNICATION_ARCHIVE_RECORDS
    ):
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath

        assert not former_path.exists()
        assert archive_path.is_file()
        assert archive_path.name.endswith(".py.legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )

        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        assert _git_blob_id(payload, path=former_relpath) == expected_blob
        assert _git_blob_id(payload, path=archive_relpath) == expected_blob
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem,
                [str(archive_path.parent)],
            )
            is None
        )

    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )

    for source_path in _repository_live_python_paths():
        assert "legacy_quarantine" not in _imported_top_level_roots(source_path)
        assert "legacy_quarantine" not in _literal_dynamic_import_roots(source_path)


def test_f06e_communication_production_caller_containment() -> None:
    """Communication archives have no live production or configured caller."""

    tracked_python_paths = _repository_live_python_paths()
    importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in tracked_python_paths
        if "communication" in _imported_top_level_roots(path)
    }
    dynamic_importers = {
        path.relative_to(_REPOSITORY_ROOT).as_posix()
        for path in tracked_python_paths
        if "communication" in _literal_dynamic_import_roots(path)
    }
    configured_importers = {
        relpath for relpath in importers if relpath.startswith("tests/tests/")
    }
    excluded_test_importers = {
        relpath
        for relpath in importers
        if relpath.startswith("tests/")
        and not relpath.startswith("tests/tests/")
    }
    production_importers = {
        relpath for relpath in importers if not relpath.startswith("tests/")
    }
    canonical_importers = {
        relpath
        for relpath in production_importers
        if relpath == "run_jaos.py"
        or relpath.startswith(("jaos/", "jaos_platform/"))
    }

    assert not (_REPOSITORY_ROOT / "communication").exists()
    assert canonical_importers == set()
    assert production_importers == set()
    assert configured_importers == set()
    assert dynamic_importers == set()
    assert excluded_test_importers == _F06E_COMMUNICATION_EXCLUDED_TEST_IMPORTERS
    assert all(
        (_REPOSITORY_ROOT / archive_relpath).is_file()
        for _former, archive_relpath, _sha256, _blob in (
            _F06E_COMMUNICATION_ARCHIVE_RECORDS
        )
    )

_F06E_SATELLITE_PRODUCTION_ROOTS = frozenset(
    {"development", "infrastructure", "pc_control"}
)
_F06E_SATELLITE_PRODUCTION_ARCHIVE_RECORDS = (
    (
        "development/__init__.py",
        "legacy_quarantine/production/development/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "development/build_test_manager.py",
        "legacy_quarantine/production/development/build_test_manager.py.legacy",
        "06fdfbf986d1b19780849e6838f1d172db6b55c75c0bb3ae866deb14dc2130a3",
        "7b639749e046f72b7ed136883624f3df801c3e49",
    ),
    (
        "development/development_workspace_manager.py",
        "legacy_quarantine/production/development/development_workspace_manager.py.legacy",
        "7d79d7cb5728b37be110d60cb1d8b9466f6227bb2383732ac49a006e9980459f",
        "b76b22ddd940ccf2b34b87dcb0a6f2436ed00e2f",
    ),
    (
        "development/git_manager.py",
        "legacy_quarantine/production/development/git_manager.py.legacy",
        "a2f04a2e1bdcc5e13d2255fa50838c990fa4d2b5de2d684533bf17992e525257",
        "ad3fbda7ff8aa614750ae1e6f046ad183211fbde",
    ),
    (
        "development/github_manager.py",
        "legacy_quarantine/production/development/github_manager.py.legacy",
        "127c256a0efba8bdb82aa52af4741b1ea7aa7c876603b091f31390530028446d",
        "51f69adf0f0cfdda9df3282a6fb6757fe36d70d5",
    ),
    (
        "development/repository_manager.py",
        "legacy_quarantine/production/development/repository_manager.py.legacy",
        "0dc11b690c3f7ffcd2763cf239973d8c0872ee8ff99d3444d469f7fc05e4f5c4",
        "bd814f05ab90c0398c66254b46c07b96edb58948",
    ),
    (
        "development/vscode_manager.py",
        "legacy_quarantine/production/development/vscode_manager.py.legacy",
        "e3a6ff01bf709b8b15c7850f8bba30162463b088b9070cc3f37fa0d9eb9a0401",
        "a4a3b4f8ede5e0044df1579e94486cfc42a99221",
    ),
    (
        "infrastructure/__init__.py",
        "legacy_quarantine/production/infrastructure/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "infrastructure/ai_provider_manager.py",
        "legacy_quarantine/production/infrastructure/ai_provider_manager.py.legacy",
        "07efd3d37b5a4837b8fe34bb33d9400416993c352896b0e0d989a1e74a3142f7",
        "b14629f344f4e45160da6a8af602b82d7ec79bd2",
    ),
    (
        "infrastructure/api_intelligence_manager.py",
        "legacy_quarantine/production/infrastructure/api_intelligence_manager.py.legacy",
        "2ede184c92bdaf1b8a8a66121562fed25462899fa5f9f4d5f5e9fdfbf105fe3a",
        "b7a1a49540572714597edfd43b215f34c9f02fb4",
    ),
    (
        "infrastructure/cost_performance_optimizer.py",
        "legacy_quarantine/production/infrastructure/cost_performance_optimizer.py.legacy",
        "0a09c48ac06f18651c45325d0bd2119539ccc5a0fed7187322bde812283381df",
        "bbd23fd3fa6b115d6f31a655b6d693a57c1de501",
    ),
    (
        "infrastructure/database_intelligence.py",
        "legacy_quarantine/production/infrastructure/database_intelligence.py.legacy",
        "d6ae6833ea8d1b5b825e945b54dab329d51888f8aec8e1316cf23bd8b5835c54",
        "b5744255dc054f40e6f3eb4be9083ea3cb4279cc",
    ),
    (
        "infrastructure/infrastructure_intelligence_core.py",
        "legacy_quarantine/production/infrastructure/infrastructure_intelligence_core.py.legacy",
        "70376a5b24a3bbc98403e2e306f4bc86ffaa0167b55b91a7571bc2899b95ad06",
        "3f008fdd954a02520ef45936a543e3637a14a593",
    ),
    (
        "infrastructure/intelligent_resource_orchestrator.py",
        "legacy_quarantine/production/infrastructure/intelligent_resource_orchestrator.py.legacy",
        "cd0ac6a3632aa160a07d60f8ca7e3373d3dec97f7340f24a445745294b7a354e",
        "465aaae65641df53d02b91a096206dbdb665de77",
    ),
    (
        "infrastructure/multi_provider_task_composer.py",
        "legacy_quarantine/production/infrastructure/multi_provider_task_composer.py.legacy",
        "e570622c0537028fc4f3c7d6dc2e2faf1164d44d87a6b81afb41e199b14db209",
        "437cebc9889498d1734f2aeba2e329dc99f71227",
    ),
    (
        "infrastructure/storage_intelligence.py",
        "legacy_quarantine/production/infrastructure/storage_intelligence.py.legacy",
        "6eb8dcc67cfe0ae4ddc0b6f7015554e1e42834ccd0373a615f44834b93989243",
        "0ae20f977b9b0f64cf5d0976ddb17970153bda02",
    ),
    (
        "pc_control/__init__.py",
        "legacy_quarantine/production/pc_control/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "pc_control/application_manager.py",
        "legacy_quarantine/production/pc_control/application_manager.py.legacy",
        "d77a2a04047212056c837a11ea865ca44565ed2aa6ce8b2ac7d3f7d00cc91c0e",
        "804215022857d6e98bc34e5ccb901b9403682101",
    ),
    (
        "pc_control/browser_controller.py",
        "legacy_quarantine/production/pc_control/browser_controller.py.legacy",
        "cd390fc8b2d5f4ee1f360639bd7a4515799d0bed3e50115f50dcf1ff70cb6e97",
        "771bf54ada23504aed7d612cc097451c460b3e2c",
    ),
    (
        "pc_control/file_system_manager.py",
        "legacy_quarantine/production/pc_control/file_system_manager.py.legacy",
        "f2cc9bc795d4b233dca7dd6f1c5b499d09f51175c42b421521f7b53ec85a8c3f",
        "fe32d3bd19e8f9432173f7b1e1f9913f777fb37c",
    ),
    (
        "pc_control/notification_manager.py",
        "legacy_quarantine/production/pc_control/notification_manager.py.legacy",
        "a4db064b6af39bd96ff7d83720e70788fd5a8b65833e2f78567322b08253aa7b",
        "07170c20957ba0bbbb7384b52f53d4de2278b7a2",
    ),
    (
        "pc_control/system_monitor.py",
        "legacy_quarantine/production/pc_control/system_monitor.py.legacy",
        "dd48ede8aeba5b953c29792c858088e4ed92a0a302dcf7dffb0a56b81178f991",
        "cae034fac3af405515c6e587c529b7f484aa0cb2",
    ),
    (
        "pc_control/terminal_controller.py",
        "legacy_quarantine/production/pc_control/terminal_controller.py.legacy",
        "29c1d5b7b8b0a1df87311d20459358cd30ee8611af42b20a0326926327874aa4",
        "485f09d21af144053da8c7dae9a87abe114a37aa",
    ),
    (
        "pc_control/window_manager.py",
        "legacy_quarantine/production/pc_control/window_manager.py.legacy",
        "d5a9c99b822213b998b688f7a998a1efd3c30ebfa00cb3a83c88277f31f85a89",
        "0cbec39e03b321703de8ec79173531dc475fdba4",
    ),
)
_F06E_SATELLITE_EXCLUDED_IMPORT_STATEMENTS = {
    "tests/ai_provider_manager_test.py": (
        ("infrastructure.ai_provider_manager",),
    ),
    "tests/api_intelligence_manager_test.py": (
        ("infrastructure.api_intelligence_manager",),
    ),
    "tests/application_manager_test.py": (
        ("pc_control.application_manager",),
    ),
    "tests/browser_controller_test.py": (
        ("pc_control.browser_controller",),
    ),
    "tests/build_test_manager_test.py": (
        ("development.build_test_manager",),
    ),
    "tests/cost_performance_optimizer_test.py": (
        ("infrastructure.cost_performance_optimizer",),
    ),
    "tests/database_intelligence_test.py": (
        ("infrastructure.database_intelligence",),
    ),
    "tests/development_platform_integration_test.py": (
        ("development.build_test_manager",),
        ("development.development_workspace_manager",),
        ("development.git_manager",),
        ("development.github_manager",),
        ("development.repository_manager",),
        ("development.vscode_manager",),
    ),
    "tests/development_workspace_manager_test.py": (
        ("development.development_workspace_manager",),
    ),
    "tests/file_system_manager_test.py": (
        ("pc_control.file_system_manager",),
    ),
    "tests/git_manager_test.py": (
        ("development.git_manager",),
    ),
    "tests/github_manager_test.py": (
        ("development.github_manager",),
    ),
    "tests/infrastructure_intelligence_core_test.py": (
        ("infrastructure.infrastructure_intelligence_core",),
    ),
    "tests/infrastructure_platform_integration_test.py": (
        ("infrastructure.ai_provider_manager",),
        ("infrastructure.api_intelligence_manager",),
        ("infrastructure.cost_performance_optimizer",),
        ("infrastructure.database_intelligence",),
        ("infrastructure.infrastructure_intelligence_core",),
        ("infrastructure.intelligent_resource_orchestrator",),
        ("infrastructure.multi_provider_task_composer",),
        ("infrastructure.storage_intelligence",),
    ),
    "tests/intelligent_resource_orchestrator_test.py": (
        ("infrastructure.intelligent_resource_orchestrator",),
    ),
    "tests/multi_provider_task_composer_test.py": (
        ("infrastructure.multi_provider_task_composer",),
    ),
    "tests/notification_manager_test.py": (
        ("pc_control.notification_manager",),
    ),
    "tests/pc_control_platform_integration_test.py": (
        ("pc_control.application_manager",),
        ("pc_control.browser_controller",),
        ("pc_control.file_system_manager",),
        ("pc_control.notification_manager",),
        ("pc_control.system_monitor",),
        ("pc_control.terminal_controller",),
        ("pc_control.window_manager",),
    ),
    "tests/repository_manager_test.py": (
        ("development.repository_manager",),
    ),
    "tests/storage_intelligence_test.py": (
        ("infrastructure.storage_intelligence",),
    ),
    "tests/system_monitor_test.py": (
        ("pc_control.system_monitor",),
    ),
    "tests/terminal_controller_test.py": (
        ("pc_control.terminal_controller",),
    ),
    "tests/vscode_manager_test.py": (
        ("development.vscode_manager",),
    ),
    "tests/window_manager_test.py": (
        ("pc_control.window_manager",),
    ),
}
_F06E_SATELLITE_RETAINED_ROOT_HASHES = {
    "dashboard": (7, "f939e8a406238bdf5060a3b87eff7e7a27f7e906e55adae01c4dbc4cc5fc3bd8"),
    "knowledge": (7, "3016bc22fe445c563416c13631da25f14b71a63fe6dfcbf443e086490bd82a29"),
    "security": (7, "37a64451143ed1fbbe3a778c622f3a86f76442691faac55c6f479ba9964a69ec"),
    "system_services": (8, "6d0ce11f46ba90802c66a463e80613e603b677cccf09b4233581eaae248aa83c"),
    "engineering": (14, "9c4a77d82edd870acc2c33ae1c5cb39d939063115c63abaf26768fc0b8298c76"),
    "workflow": (9, "0f65197fe64f5eff0753c4277ea8cbf320c19426aa752215bfe6793eb4577d35"),
}


def test_f06e_satellite_production_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """The 24 production payloads are exact, inert, and reversible archives."""

    _assert_f06e_production_archive_payloads(
        _F06E_SATELLITE_PRODUCTION_ARCHIVE_RECORDS,
        {"development": 7, "infrastructure": 9, "pc_control": 8},
        pytestconfig,
    )


def _assert_f06e_production_archive_payloads(
    records: tuple[tuple[str, str, str, str], ...],
    expected_counts: dict[str, int],
    pytestconfig: pytest.Config,
) -> None:
    """Apply the established production archive guard to an exact slice."""

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    expected_total = sum(expected_counts.values())
    assert len(records) == expected_total
    assert len({record[0] for record in records}) == expected_total
    assert len({record[1] for record in records}) == expected_total

    for root_name, expected_count in expected_counts.items():
        assert not (_REPOSITORY_ROOT / root_name).exists()
        root_records = tuple(r for r in records if r[0].startswith(root_name + "/"))
        assert len(root_records) == expected_count
        archive_root = _REPOSITORY_ROOT / "legacy_quarantine/production" / root_name
        expected_entries = {record[1] for record in root_records}
        for _former, archive, _sha256, _blob in root_records:
            parent = (_REPOSITORY_ROOT / archive).parent
            while parent != archive_root:
                expected_entries.add(parent.relative_to(_REPOSITORY_ROOT).as_posix())
                parent = parent.parent
        assert {
            path.relative_to(_REPOSITORY_ROOT).as_posix()
            for path in archive_root.rglob("*")
        } == expected_entries
        assert (
            importlib.machinery.PathFinder.find_spec(
                root_name, [str(_REPOSITORY_ROOT)]
            )
            is None
        )

    for former_relpath, archive_relpath, expected_sha256, expected_blob in records:
        former_path = _REPOSITORY_ROOT / former_relpath
        archive_path = _REPOSITORY_ROOT / archive_relpath
        assert archive_relpath == f"legacy_quarantine/production/{former_relpath}.legacy"
        assert not former_path.exists()
        assert archive_path.is_file()
        assert not archive_path.is_symlink()
        assert former_path.suffix in {".py", ".md"}
        assert archive_path.name.endswith(former_path.suffix + ".legacy")
        assert not archive_path.name.endswith(import_suffixes)
        assert not any(
            fnmatch.fnmatchcase(archive_path.name, pattern)
            for pattern in python_file_patterns
        )
        payload = archive_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_sha256
        assert _git_blob_id(payload, path=former_relpath) == expected_blob
        assert _git_blob_id(payload, path=archive_relpath) == expected_blob
        assert (
            importlib.machinery.PathFinder.find_spec(
                former_path.stem, [str(archive_path.parent)]
            )
            is None
        )

    assert not tuple(
        (_REPOSITORY_ROOT / "legacy_quarantine").rglob("__init__.py")
    )
    for source_path in _repository_live_python_paths():
        assert "legacy_quarantine" not in _imported_top_level_roots(source_path)
        assert "legacy_quarantine" not in _literal_dynamic_import_roots(source_path)


def test_f06e_satellite_production_caller_and_boundary_containment() -> None:
    """Only the exact excluded debt refers to the three retired production roots."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    roots = _F06E_SATELLITE_PRODUCTION_ROOTS
    paths = _repository_live_python_paths()
    observed: dict[str, tuple[tuple[str, ...], ...]] = {}
    for path in paths:
        statements = []
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            names: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = (node.module,)
            matching = tuple(name for name in names if name.partition(".")[0] in roots)
            if matching:
                statements.append(matching)
        if statements:
            observed[path.relative_to(_REPOSITORY_ROOT).as_posix()] = tuple(statements)
        assert not roots & _literal_dynamic_import_roots(path)

    canonical = {
        path for path in observed
        if path == "run_jaos.py" or path.startswith(("jaos/", "jaos_platform/"))
    }
    production = {path for path in observed if not path.startswith("tests/")}
    configured = {path for path in observed if path.startswith("tests/tests/")}
    assert canonical == set()
    assert production == set()
    assert configured == set()
    assert observed == _F06E_SATELLITE_EXCLUDED_IMPORT_STATEMENTS
    assert len(observed) == 24
    assert sum(len(statements) for statements in observed.values()) == 42
    for root_name, expected in {
        "development": (7, 12),
        "infrastructure": (9, 16),
        "pc_control": (8, 14),
    }.items():
        per_root = {
            path: tuple(
                statement for statement in statements
                if any(name.partition(".")[0] == root_name for name in statement)
            )
            for path, statements in observed.items()
        }
        assert (
            sum(bool(statements) for statements in per_root.values()),
            sum(len(statements) for statements in per_root.values()),
        ) == expected

    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert not roots & {
        module.partition(".")[0] for module in closure["reached_modules"]
    }

    configured_paths = tuple(
        path for path in paths
        if path.relative_to(_REPOSITORY_ROOT).as_posix().startswith("tests/tests/")
    )
    legacy_facing = {
        path for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    }
    assert legacy_facing == {_F06D_CONFIG_CONTAINMENT_PATH}
    assert _F06D_CONFIG_CONTAINMENT_PATH in configured_paths
    assert not any(
        "executive_brain" in _imported_top_level_roots(path)
        for path in configured_paths
    )
    _assert_config_containment_preserved()

    _assert_f06e_satellite_retained_inventory()


def _assert_f06e_satellite_retained_inventory() -> None:
    """Preserve former source inventories through exact archives after retirement."""

    for root_name, (expected_count, expected_digest) in (
        _F06E_SATELLITE_RETAINED_ROOT_HASHES.items()
    ):
        if root_name in _F06E_DYNAMIC_SATELLITE_PRODUCTION_ROOTS | {"engineering"}:
            records = tuple(
                record for record in (
                    _F06E_DYNAMIC_SATELLITE_ARCHIVE_RECORDS
                    + _F06E_ENGINEERING_ARCHIVE_RECORDS
                )
                if record[0].startswith(root_name + "/")
            )
            assert len(records) == expected_count
            assert not (_REPOSITORY_ROOT / root_name).exists()
            inventory = "".join(
                former + "\0"
                + hashlib.sha256((_REPOSITORY_ROOT / archive).read_bytes()).hexdigest()
                + "\n"
                for former, archive, _sha256, _blob in sorted(records)
            )
            assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == expected_digest
            continue
        retained_paths = sorted(
            path for path in (_REPOSITORY_ROOT / root_name).rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        )
        assert len(retained_paths) == expected_count
        inventory = "".join(
            path.relative_to(_REPOSITORY_ROOT).as_posix()
            + "\0" + hashlib.sha256(path.read_bytes()).hexdigest() + "\n"
            for path in retained_paths
        )
        assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == expected_digest


_F06E_DYNAMIC_SATELLITE_PRODUCTION_ROOTS = frozenset(
    {"dashboard", "knowledge", "security", "system_services"}
)
_F06E_DYNAMIC_SATELLITE_ARCHIVE_RECORDS = (
    (
        "dashboard/__init__.py",
        "legacy_quarantine/production/dashboard/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "dashboard/action_timeline.py",
        "legacy_quarantine/production/dashboard/action_timeline.py.legacy",
        "10480d72d139275b1238e2784079375f5888f670038d44e55efdeb7c5740a476",
        "c4c537e3a79b8378f921e8a03e2e5292c7c687b9",
    ),
    (
        "dashboard/capability_viewer.py",
        "legacy_quarantine/production/dashboard/capability_viewer.py.legacy",
        "e0be93481d37e8f10e18d1e70b2440ee8ae452ba24158e194092cac79a0386db",
        "58d2cc7e53120e07be525a39760e8cb02ba22103",
    ),
    (
        "dashboard/mission_control.py",
        "legacy_quarantine/production/dashboard/mission_control.py.legacy",
        "a73958d4944a04f78154836872227b22e1516ff9a6eee7b0f8568f92334d9989",
        "b3920709eb0d700dd8eea45d1c861691437d5029",
    ),
    (
        "dashboard/notification_center.py",
        "legacy_quarantine/production/dashboard/notification_center.py.legacy",
        "9ea544bd133670f720493a33ac992af762155ffd7a362761011f9d3c494aa92b",
        "8e4b8742f91f075baa4bef609396134f43d3f3dd",
    ),
    (
        "dashboard/platform_status_dashboard.py",
        "legacy_quarantine/production/dashboard/platform_status_dashboard.py.legacy",
        "31779d7ea5bd7c2f692dd23ac7dc3294333c1cee7422081ea5a7f39f97945e4d",
        "a0237b32d2fef1e4b9106f4cf6895717a1490594",
    ),
    (
        "dashboard/system_health_dashboard.py",
        "legacy_quarantine/production/dashboard/system_health_dashboard.py.legacy",
        "c04f683a92c491edf20303d2bd7982adb4866c1ab1b06de486021cb2f69def4f",
        "e9c085d56097f060870df66acc56118d37a10140",
    ),
    (
        "knowledge/__init__.py",
        "legacy_quarantine/production/knowledge/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "knowledge/document_manager.py",
        "legacy_quarantine/production/knowledge/document_manager.py.legacy",
        "43eda5b09f5d79359a5b712f7b235cf33843d7984c7ac6fdf2ff21f6c6043175",
        "619f5f2924f4f08357df9f9388e1c677824544e9",
    ),
    (
        "knowledge/knowledge_base.py",
        "legacy_quarantine/production/knowledge/knowledge_base.py.legacy",
        "ee77f8dae0dcfdbbfd27f659ee59c492f18849376e3e326adfc78c08d4e35db0",
        "19e4e41a456080fbf59b66f543a3b52005b2866d",
    ),
    (
        "knowledge/knowledge_graph.py",
        "legacy_quarantine/production/knowledge/knowledge_graph.py.legacy",
        "474167d74cddae05211f60b7bd25c8d6318474328899a0da76af88ca21626726",
        "cb893f4219b2acf600e8c748992769270ed1ed20",
    ),
    (
        "knowledge/learning_synchronizer.py",
        "legacy_quarantine/production/knowledge/learning_synchronizer.py.legacy",
        "e4d208d8819c3756a41869c4c83d46e95ae12a46ac3cae8689fd0c3038ac896e",
        "2c7581746f092c428a795bb2924b17513f5474df",
    ),
    (
        "knowledge/ocr_manager.py",
        "legacy_quarantine/production/knowledge/ocr_manager.py.legacy",
        "ed713c0a8d3a3a110b8137896c79a74781338ef6b20331e5d48eafd9273e97cc",
        "d01852ef87c5da54a7b2a8d5a5901e1b232f1e1c",
    ),
    (
        "knowledge/research_manager.py",
        "legacy_quarantine/production/knowledge/research_manager.py.legacy",
        "56ddc816a9a61ceee53df03e3722a1ee9cf558d7daa42746ac5f5f14f4107ef9",
        "a50ad601e2a7e20be6a9de8080a33c70bcb0c930",
    ),
    (
        "security/__init__.py",
        "legacy_quarantine/production/security/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "security/audit_logger.py",
        "legacy_quarantine/production/security/audit_logger.py.legacy",
        "e2b3da6feee771808c94fcadc45309ed8e74be29c331e3d9879d4cee77656649",
        "188ba9ce48cf2ea773bb6a97febc1b88a63f41a0",
    ),
    (
        "security/authentication_manager.py",
        "legacy_quarantine/production/security/authentication_manager.py.legacy",
        "e3c09581d762e71e0fb81e41b52b4fcfeb61fc93906ea5b25637fe19d942c2d8",
        "35dab4a63e96a68d0d5a34571aac41bc41aff195",
    ),
    (
        "security/authorization_manager.py",
        "legacy_quarantine/production/security/authorization_manager.py.legacy",
        "da1f03b10c71b962c199a75b1712e406b36b299958f73ffb470d475d39c1632c",
        "5e4758bf6d0fd1fd879619ec3dfb0369a95d4027",
    ),
    (
        "security/identity_manager.py",
        "legacy_quarantine/production/security/identity_manager.py.legacy",
        "27183e3775239b6c17f910a19144e595f28c477fe1151d1cc137fb3c607bb4c1",
        "060e1ff57c54d6f2236f9433236ff642fded86ab",
    ),
    (
        "security/permission_manager.py",
        "legacy_quarantine/production/security/permission_manager.py.legacy",
        "3d6e374399115292e175c696fdaf3fc37211ef472a43aacb30f6380ecbe6160b",
        "98cf266fd3906d93ec9016987fcd329b7854bddf",
    ),
    (
        "security/security_monitor.py",
        "legacy_quarantine/production/security/security_monitor.py.legacy",
        "df81267649ba9ca8f00613e37214af45130b58ed8018968b46f12c3e879b244c",
        "75f3c2c9ea2ac26da3d4902b6b3fcee81774f5c5",
    ),
    (
        "system_services/__init__.py",
        "legacy_quarantine/production/system_services/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "system_services/backup_manager.py",
        "legacy_quarantine/production/system_services/backup_manager.py.legacy",
        "2363a9c574a57420f3a9713b86a3090f7565df272356c320b7d35370979733e7",
        "bacee2a048354455599271602adfa36e31ca605f",
    ),
    (
        "system_services/cache_manager.py",
        "legacy_quarantine/production/system_services/cache_manager.py.legacy",
        "18208fa63f7371582824891efce046930456e3e3196e993a5bee50e51b77f6a6",
        "867751a0ce7c73d594122e619c9acb33116bc2b6",
    ),
    (
        "system_services/cleanup_manager.py",
        "legacy_quarantine/production/system_services/cleanup_manager.py.legacy",
        "e21c4506267731644a9e57f5742090bf1c4427282cf558063e76741507ab265a",
        "a9fc5bf27009fa49f14ac2b4490231d82a0df3da",
    ),
    (
        "system_services/configuration_manager.py",
        "legacy_quarantine/production/system_services/configuration_manager.py.legacy",
        "8d6217b9a2b788792cc34247b71687bd1cd1d0ea579fa96010f8f49a117893f7",
        "200a0b9114352833fc8525f563c0c8cabc89a2b6",
    ),
    (
        "system_services/scheduler.py",
        "legacy_quarantine/production/system_services/scheduler.py.legacy",
        "179d173bdd2ca70d5470fad407c804350589f261760e7789052e601d1e2a762a",
        "e7253b39c6ffc686697957338e7285abfed81ce2",
    ),
    (
        "system_services/startup_manager.py",
        "legacy_quarantine/production/system_services/startup_manager.py.legacy",
        "fa6ce315391ff114aaafe30792ae865b21bc0ba63794e641956a213358f990b0",
        "19794eaa15a69d2df5dd168d87f0f561d29bf8ad",
    ),
    (
        "system_services/update_manager.py",
        "legacy_quarantine/production/system_services/update_manager.py.legacy",
        "479ba26e1a1e5f2c4b9c1b559da97165c9bd063f6376ad1f5f314d3d1fe4ad7b",
        "6066cb60c167c6b33f7d2e4bc7df735ee2759a17",
    ),
)
_F06E_DYNAMIC_SATELLITE_EXCLUDED_IMPORT_STATEMENTS = {
    "tests/action_timeline_test.py": (
        ("dashboard.action_timeline",),
    ),
    "tests/audit_logger_test.py": (
        ("security.audit_logger",),
    ),
    "tests/authentication_manager_test.py": (
        ("security.authentication_manager",),
    ),
    "tests/authorization_manager_test.py": (
        ("security.authorization_manager",),
    ),
    "tests/backup_manager_test.py": (
        ("system_services.backup_manager",),
    ),
    "tests/cache_manager_test.py": (
        ("system_services.cache_manager",),
    ),
    "tests/capability_viewer_test.py": (
        ("dashboard.capability_viewer",),
    ),
    "tests/cleanup_manager_test.py": (
        ("system_services.cleanup_manager",),
    ),
    "tests/configuration_manager_test.py": (
        ("system_services.configuration_manager",),
    ),
    "tests/dashboard_platform_integration_test.py": (
        ("dashboard.action_timeline",),
        ("dashboard.capability_viewer",),
        ("dashboard.mission_control",),
        ("dashboard.notification_center",),
        ("dashboard.platform_status_dashboard",),
        ("dashboard.system_health_dashboard",),
    ),
    "tests/document_manager_test.py": (
        ("knowledge.document_manager",),
    ),
    "tests/identity_manager_test.py": (
        ("security.identity_manager",),
    ),
    "tests/knowledge_base_test.py": (
        ("knowledge.knowledge_base",),
    ),
    "tests/knowledge_graph_test.py": (
        ("knowledge.knowledge_graph",),
    ),
    "tests/knowledge_platform_integration_test.py": (
        ("knowledge.document_manager",),
        ("knowledge.knowledge_base",),
        ("knowledge.knowledge_graph",),
        ("knowledge.learning_synchronizer",),
        ("knowledge.ocr_manager",),
        ("knowledge.research_manager",),
    ),
    "tests/learning_synchronizer_test.py": (
        ("knowledge.learning_synchronizer",),
    ),
    "tests/mission_control_test.py": (
        ("dashboard.mission_control",),
    ),
    "tests/notification_center_test.py": (
        ("dashboard.notification_center",),
    ),
    "tests/ocr_manager_test.py": (
        ("knowledge.ocr_manager",),
    ),
    "tests/permission_manager_test.py": (
        ("security.permission_manager",),
    ),
    "tests/platform_status_dashboard_test.py": (
        ("dashboard.platform_status_dashboard",),
    ),
    "tests/research_manager_test.py": (
        ("knowledge.research_manager",),
    ),
    "tests/scheduler_test.py": (
        ("system_services.scheduler",),
    ),
    "tests/security_monitor_test.py": (
        ("security.security_monitor",),
    ),
    "tests/security_platform_integration_test.py": (
        ("security.audit_logger",),
        ("security.authentication_manager",),
        ("security.authorization_manager",),
        ("security.identity_manager",),
        ("security.permission_manager",),
        ("security.security_monitor",),
    ),
    "tests/startup_manager_test.py": (
        ("system_services.startup_manager",),
    ),
    "tests/system_health_dashboard_test.py": (
        ("dashboard.system_health_dashboard",),
    ),
    "tests/system_services_integration_test.py": (
        ("system_services.backup_manager",),
        ("system_services.cache_manager",),
        ("system_services.cleanup_manager",),
        ("system_services.configuration_manager",),
        ("system_services.scheduler",),
        ("system_services.startup_manager",),
        ("system_services.update_manager",),
    ),
    "tests/update_manager_test.py": (
        ("system_services.update_manager",),
    ),
}
_F06E_DYNAMIC_SATELLITE_REGISTRATIONS = (
    ("tests/engineering_platform_integration_test.py", 46, "security.permission_manager"),
    ("tests/import_validator_test.py", 5, "security.permission_manager"),
    ("tests/import_validator_test.py", 6, "dashboard.mission_control"),
    ("tests/import_validator_test.py", 7, "system_services.backup_manager"),
    ("tests/import_validator_test.py", 8, "knowledge.knowledge_graph"),
)
_F06E_DYNAMIC_SATELLITE_EXCLUDED_SCRIPT_HASHES = {
    "tests/import_validator_test.py":
        "a5eb354d111606d6ec4bf8b976294a6b819e0d048640918e4adedba86eb453ac",
    "tests/engineering_platform_integration_test.py":
        "45a57aabeebbd4a9e3ea33fe742f213230757fe2fd90284667c9462a96197c1e",
    "tests/project_structure_validator_test.py":
        "3dc2a18c223a4257c9728e824feedc2a4fd3d4356c02a62e05ccc8699c3e0f51",
}


def test_f06e_dynamic_satellite_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """The 29 adjudicated satellite payloads remain exact, inert archives."""

    _assert_f06e_production_archive_payloads(
        _F06E_DYNAMIC_SATELLITE_ARCHIVE_RECORDS,
        {"dashboard": 7, "knowledge": 7, "security": 7, "system_services": 8},
        pytestconfig,
    )
    _assert_f06e_satellite_retained_inventory()


def test_f06e_dynamic_satellite_caller_and_boundary_containment() -> None:
    """Only the exact excluded import, registration, and folder debt remains."""

    _assert_f06e_dynamic_satellite_caller_and_boundary_containment()


def _assert_f06e_dynamic_satellite_caller_and_boundary_containment() -> None:
    """Retain dynamic registration and folder-validation debt across retirements."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    roots = _F06E_DYNAMIC_SATELLITE_PRODUCTION_ROOTS
    paths = _repository_live_python_paths()
    observed: dict[str, tuple[tuple[str, ...], ...]] = {}
    registrations = []
    validator_callers: set[str] = set()
    structure_callers: set[str] = set()
    dynamic_files: set[str] = set()
    excluded_scripts = set(_F06E_DYNAMIC_SATELLITE_EXCLUDED_SCRIPT_HASHES)
    excluded_modules = {
        path.removesuffix(".py").replace("/", ".") for path in excluded_scripts
    }
    for path in paths:
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        statements = []
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            names: tuple[str, ...] = ()
            imported_names: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                names = imported_names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = (node.module,)
                imported_names = names + tuple(
                    node.module + "." + alias.name for alias in node.names
                )
            matching = tuple(name for name in names if name.partition(".")[0] in roots)
            if matching:
                statements.append(matching)
            for name in imported_names:
                if name == "engineering.import_validator" or name.startswith(
                    "engineering.import_validator."
                ):
                    validator_callers.add(relpath)
                if name == "engineering.project_structure_validator" or name.startswith(
                    "engineering.project_structure_validator."
                ):
                    structure_callers.add(relpath)
                assert not any(
                    name == module or name.startswith(module + ".")
                    for module in excluded_modules
                ), (relpath, name)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_import"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and node.args[0].value.partition(".")[0] in roots
            ):
                registrations.append((relpath, node.lineno, node.args[0].value))
        if statements:
            observed[relpath] = tuple(statements)
        if roots & _literal_dynamic_import_roots(path):
            dynamic_files.add(relpath)

    assert observed == _F06E_DYNAMIC_SATELLITE_EXCLUDED_IMPORT_STATEMENTS
    assert len(observed) == 29
    assert sum(map(len, observed.values())) == 50
    assert not {p for p in observed if not p.startswith("tests/")}
    assert not {p for p in observed if p.startswith("tests/tests/")}
    assert not {
        p for p in observed
        if p == "run_jaos.py" or p.startswith(("jaos/", "jaos_platform/"))
    }
    assert tuple(sorted(registrations)) == _F06E_DYNAMIC_SATELLITE_REGISTRATIONS
    assert len(registrations) == 5
    assert dynamic_files == validator_callers == {
        "tests/import_validator_test.py",
        "tests/engineering_platform_integration_test.py",
    }
    assert structure_callers == {
        "tests/project_structure_validator_test.py",
        "tests/engineering_platform_integration_test.py",
    }
    for root_name, expected in {
        "dashboard": (7, 12, 1),
        "knowledge": (7, 12, 1),
        "security": (7, 12, 2),
        "system_services": (8, 14, 1),
    }.items():
        counts = [
            sum(
                any(name.partition(".")[0] == root_name for name in statement)
                for statement in statements
            )
            for statements in observed.values()
        ]
        assert (
            sum(bool(count) for count in counts),
            sum(counts),
            sum(module.partition(".")[0] == root_name for _, _, module in registrations),
        ) == expected

    assert len(set(observed) | dynamic_files) == 31
    excluded_debt = set(observed) | dynamic_files | structure_callers
    assert len(excluded_debt) == 32
    tests_conftest = _load_tests_conftest()
    for relpath in excluded_debt:
        assert tests_conftest.is_excluded_legacy_module(_REPOSITORY_ROOT / relpath)
    for relpath, expected_sha256 in (
        _F06E_DYNAMIC_SATELLITE_EXCLUDED_SCRIPT_HASHES.items()
    ):
        assert hashlib.sha256(
            (_REPOSITORY_ROOT / relpath).read_bytes()
        ).hexdigest() == expected_sha256

    # Engineering archive/workflow source hashes retain the exact evidence;
    # no excluded executable script or archived loader is imported or executed.
    _assert_f06e_satellite_retained_inventory()
    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert not (roots | {"engineering"}) & {
        module.partition(".")[0] for module in closure["reached_modules"]
    }
    configured_paths = {
        path for path in paths
        if path.relative_to(_REPOSITORY_ROOT).as_posix().startswith("tests/tests/")
    }
    assert _F06D_CONFIG_CONTAINMENT_PATH in configured_paths
    assert {
        path for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    } == {_F06D_CONFIG_CONTAINMENT_PATH}
    assert not any(
        "executive_brain" in _imported_top_level_roots(path)
        for path in configured_paths
    )
    _assert_config_containment_preserved()


_F06E_ENGINEERING_ARCHIVE_RECORDS = (
    (
        "engineering/__init__.py",
        "legacy_quarantine/production/engineering/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "engineering/capability_truth_engine.py",
        "legacy_quarantine/production/engineering/capability_truth_engine.py.legacy",
        "8bf1bf8e0e6d142c6538631cc97a99c887fc45419a6f8a56351253ff6d27afc2",
        "e909ca3db8fe262d218a3ee8977e905a3dadf8cb",
    ),
    (
        "engineering/configuration_validator.py",
        "legacy_quarantine/production/engineering/configuration_validator.py.legacy",
        "33863a72231b920503cde328770e160dac49c347e298a19dfeb03e6cccc7f852",
        "8be30d920d3309a02cc2f855af4811c6cce5029a",
    ),
    (
        "engineering/dependency_validator.py",
        "legacy_quarantine/production/engineering/dependency_validator.py.legacy",
        "4700288929eb6ed2c57229412b3354183b54eca9c24b36e7bb77204f403e277c",
        "6d5b0d27654a0b637fa72a8095b94caf67eb0d4d",
    ),
    (
        "engineering/engineering_report_generator.py",
        "legacy_quarantine/production/engineering/engineering_report_generator.py.legacy",
        "ee0451839f923fb75998d10a11ccdcbac9dd9cee60cd144eb17bbe1d1aca7d4e",
        "15fb94bf179839fd67fcf07fca925597b7a7f470",
    ),
    (
        "engineering/import_validator.py",
        "legacy_quarantine/production/engineering/import_validator.py.legacy",
        "9a79d5c0093bb1eb01cf8f2cce651b4f7aa214b2dd33345bc4d57f5936346a32",
        "38e9d2584bd1da71ebe2797dca166384e2595d02",
    ),
    (
        "engineering/integration_test_runner.py",
        "legacy_quarantine/production/engineering/integration_test_runner.py.legacy",
        "9a54364f00f2316a49a4b1e2becdeeb1127c81b9009082b9ff138c8b0abac9d5",
        "08c9a2be80d5126fb91d772040852e6c7cf837e7",
    ),
    (
        "engineering/module_registry.py",
        "legacy_quarantine/production/engineering/module_registry.py.legacy",
        "71f1409fab6ab7137ed8db681d65c47389a9ef669074954fa71749c39a23cba1",
        "f22524a1c33eef4b6eacae1603791b59db26ed54",
    ),
    (
        "engineering/package_registry.py",
        "legacy_quarantine/production/engineering/package_registry.py.legacy",
        "f9a3308ee1a631d61e63b4d0b77e2d7260c7a4bc98595f14cbfde9ce47ba7d18",
        "30456374a1a4e748a1eebdde14fde5e027a25a54",
    ),
    (
        "engineering/platform_health_dashboard.py",
        "legacy_quarantine/production/engineering/platform_health_dashboard.py.legacy",
        "9be1bfc29ed0be429faccdece9260dd1f86b7ee8e6a422a99a6f9926a855c998",
        "0d8f599fd47c914602b77ff31b1c8997f62bdd0f",
    ),
    (
        "engineering/platform_registry.py",
        "legacy_quarantine/production/engineering/platform_registry.py.legacy",
        "a77251a129bfc7710468ea68ba652c11952db7759840302ab01d50821a5eb377",
        "af8233ebf94be9d87c87278a84f7d654370f2729",
    ),
    (
        "engineering/project_structure_validator.py",
        "legacy_quarantine/production/engineering/project_structure_validator.py.legacy",
        "d58f00665a0d388e7d7545648b2475d6035b3787ba6571e45fb10f46b627f350",
        "e15bd00354790aa2837b436735b18d5488b5d422",
    ),
    (
        "engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md",
        "legacy_quarantine/production/engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "engineering/startup_validator.py",
        "legacy_quarantine/production/engineering/startup_validator.py.legacy",
        "227e30ab2b285bafeaaf61ae14994305bb4b96481ce90e1d6f5a31abcdb3487e",
        "25b678c2dd5cecd427453c388a7b26afa8077117",
    ),
)
_F06E_ENGINEERING_SOURCE_SIZES = {
    "engineering/__init__.py": 0,
    "engineering/capability_truth_engine.py": 1229,
    "engineering/configuration_validator.py": 1088,
    "engineering/dependency_validator.py": 880,
    "engineering/engineering_report_generator.py": 1107,
    "engineering/import_validator.py": 1108,
    "engineering/integration_test_runner.py": 1039,
    "engineering/module_registry.py": 1084,
    "engineering/package_registry.py": 820,
    "engineering/platform_health_dashboard.py": 1879,
    "engineering/platform_registry.py": 957,
    "engineering/project_structure_validator.py": 1204,
    "engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md": 0,
    "engineering/startup_validator.py": 1693,
}
_F06E_ENGINEERING_EXCLUDED_IMPORT_STATEMENTS = {
    "tests/capability_truth_engine_test.py": (
        ("engineering.capability_truth_engine",),
    ),
    "tests/configuration_validator_test.py": (
        ("engineering.configuration_validator",),
    ),
    "tests/dependency_validator_test.py": (
        ("engineering.dependency_validator",),
    ),
    "tests/engineering_platform_integration_test.py": (
        ("engineering.capability_truth_engine",),
        ("engineering.configuration_validator",),
        ("engineering.dependency_validator",),
        ("engineering.engineering_report_generator",),
        ("engineering.import_validator",),
        ("engineering.integration_test_runner",),
        ("engineering.module_registry",),
        ("engineering.package_registry",),
        ("engineering.platform_health_dashboard",),
        ("engineering.platform_registry",),
        ("engineering.project_structure_validator",),
        ("engineering.startup_validator",),
    ),
    "tests/engineering_report_generator_test.py": (
        ("engineering.engineering_report_generator",),
    ),
    "tests/import_validator_test.py": (
        ("engineering.import_validator",),
    ),
    "tests/integration_test_runner_test.py": (
        ("engineering.integration_test_runner",),
    ),
    "tests/module_registry_test.py": (
        ("engineering.module_registry",),
    ),
    "tests/package_registry_test.py": (
        ("engineering.package_registry",),
    ),
    "tests/platform_health_dashboard_test.py": (
        ("engineering.platform_health_dashboard",),
    ),
    "tests/platform_registry_test.py": (
        ("engineering.platform_registry",),
    ),
    "tests/project_structure_validator_test.py": (
        ("engineering.project_structure_validator",),
    ),
    "tests/startup_validator_test.py": (
        ("engineering.startup_validator",),
    ),
}
_F06E_ENGINEERING_EXCLUDED_SCRIPT_HASHES = {
    "tests/capability_truth_engine_test.py":
        "c5a1e3d1b6ae781fd381d187a90e5e5a1b6029d6779cf138f447d7e0078320b5",
    "tests/configuration_validator_test.py":
        "b7c3544c17759483a036465a2c4444c59c2d7389a5bcb059fb4cb1bdc7948f81",
    "tests/dependency_validator_test.py":
        "1e16092c75de621dc0c850ccbfb35862014f5cc56a22c0fb6f198b8123da3656",
    "tests/engineering_platform_integration_test.py":
        "45a57aabeebbd4a9e3ea33fe742f213230757fe2fd90284667c9462a96197c1e",
    "tests/engineering_report_generator_test.py":
        "9de6cb00d8061971dad1590a3ca0f472c52dff45e9f0abad6d6642220325aec6",
    "tests/import_validator_test.py":
        "a5eb354d111606d6ec4bf8b976294a6b819e0d048640918e4adedba86eb453ac",
    "tests/integration_test_runner_test.py":
        "7639aaedd0e1017e5bfadd316ea65846942952c3d420e55c90529d0326968ea6",
    "tests/module_registry_test.py":
        "6be0efbc247582a7f4a6d8b6abecd7362fbb80cf7044fd626e531205864168eb",
    "tests/package_registry_test.py":
        "a7e4263885e967bc5600b42740505d7c069604b6a645d1a4a3f4e9499ddfb1ff",
    "tests/platform_health_dashboard_test.py":
        "f0c8a15ded669a296d32594c3deab1d6432310824527bca54778cd86750810c8",
    "tests/platform_registry_test.py":
        "88b786cf03cce775ad902643caf7710036f9ee03bdb901aae517ed3019ade984",
    "tests/project_structure_validator_test.py":
        "3dc2a18c223a4257c9728e824feedc2a4fd3d4356c02a62e05ccc8699c3e0f51",
    "tests/startup_validator_test.py":
        "c48482ca753fc9f75b2ced5785da9c5b3f78324187542a48fffee5b6bb574f6a",
}


def test_f06e_engineering_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """Preserve 13 Python sources and one historical Markdown artifact exactly."""

    _assert_f06e_production_archive_payloads(
        _F06E_ENGINEERING_ARCHIVE_RECORDS,
        {"engineering": 14},
        pytestconfig,
    )
    former_paths = {record[0] for record in _F06E_ENGINEERING_ARCHIVE_RECORDS}
    assert set(_F06E_ENGINEERING_SOURCE_SIZES) == former_paths
    assert sum(path.endswith(".py") for path in former_paths) == 13
    assert {path for path in former_paths if not path.endswith(".py")} == {
        "engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md",
    }
    for former, archive, _sha256, _blob in _F06E_ENGINEERING_ARCHIVE_RECORDS:
        assert (_REPOSITORY_ROOT / archive).stat().st_size == (
            _F06E_ENGINEERING_SOURCE_SIZES[former]
        )
    _assert_f06e_satellite_retained_inventory()


def test_f06e_engineering_caller_and_boundary_containment() -> None:
    """Only the exact excluded engineering debt survives production retirement."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    paths = _repository_live_python_paths()
    observed: dict[str, tuple[tuple[str, ...], ...]] = {}
    legacy_service_consumers: set[str] = set()
    excluded_modules = {
        path.removesuffix(".py").replace("/", ".")
        for path in _F06E_ENGINEERING_EXCLUDED_IMPORT_STATEMENTS
    }
    for path in paths:
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        statements = []
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            names: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = (node.module,)
            matching = tuple(
                name for name in names if name.partition(".")[0] == "engineering"
            )
            if matching:
                statements.append(matching)
            imported_names = names
            if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imported_names += tuple(
                    node.module + "." + alias.name for alias in node.names
                )
            assert not any(
                name == module or name.startswith(module + ".")
                for name in imported_names for module in excluded_modules
            ), relpath
            if any(
                name == "jaos_platform.base_platform_service"
                or name.startswith("jaos_platform.base_platform_service.")
                for name in imported_names
            ) and not relpath.startswith(("jaos/", "jaos_platform/", "tests/")):
                legacy_service_consumers.add(relpath)
            if relpath.startswith(("jaos/", "jaos_platform/")) and (
                isinstance(node, ast.Constant) and isinstance(node.value, str)
            ):
                assert node.value != "engineering"
                assert not node.value.startswith("engineering.")
        if statements:
            observed[relpath] = tuple(statements)
        assert "engineering" not in _literal_dynamic_import_roots(path)

    assert observed == _F06E_ENGINEERING_EXCLUDED_IMPORT_STATEMENTS
    assert len(observed) == 13
    assert sum(map(len, observed.values())) == 24
    assert not {path for path in observed if not path.startswith("tests/")}
    assert not {path for path in observed if path.startswith("tests/tests/")}
    assert not {
        path for path in observed
        if path == "run_jaos.py" or path.startswith(("jaos/", "jaos_platform/"))
    }
    assert legacy_service_consumers == {
        "workflow/workflow_engine.py",
        "executive_brain/memory/memory_manager.py",
    }
    tests_conftest = _load_tests_conftest()
    assert set(_F06E_ENGINEERING_EXCLUDED_SCRIPT_HASHES) == set(observed)
    for relpath, expected_sha256 in _F06E_ENGINEERING_EXCLUDED_SCRIPT_HASHES.items():
        path = _REPOSITORY_ROOT / relpath
        assert tests_conftest.is_excluded_legacy_module(path)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha256

    # Reuse the exact five registrations, both validator caller sets, excluded
    # script hashes, archive/workflow inventory, and configured config boundary.
    _assert_f06e_dynamic_satellite_caller_and_boundary_containment()
    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert "engineering" not in {
        module.partition(".")[0] for module in closure["reached_modules"]
    }
    configured_paths = {
        path for path in paths
        if path.relative_to(_REPOSITORY_ROOT).as_posix().startswith("tests/tests/")
    }
    assert _F06D_CONFIG_CONTAINMENT_PATH in configured_paths
    assert {
        path for path in configured_paths
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    } == {_F06D_CONFIG_CONTAINMENT_PATH}
    assert not any(
        "executive_brain" in _imported_top_level_roots(path)
        for path in configured_paths
    )
    _assert_config_containment_preserved()
