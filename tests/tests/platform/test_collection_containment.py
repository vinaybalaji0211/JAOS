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
        assert not (_REPOSITORY_ROOT / prototype_relpath).exists()
        record = next(
            row for row in _F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS
            if row[0] == prototype_relpath
        )
        payload = (_REPOSITORY_ROOT / record[1]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == record[2]
        assert _git_blob_id(payload, path=prototype_relpath) == record[3]


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
        assert not (_REPOSITORY_ROOT / production_relpath).exists()
        assert production_relpath in _assert_f06e_executive_historical_inventory()
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

    # F06E retired these production adapters; retain their exact original evidence.
    for production_relpath in _F06D_PROVIDER_PRODUCTION_PATHS:
        record = next(
            row for row in _F06E_EXECUTIVE_AI_ARCHIVE_RECORDS
            if row[0] == production_relpath
        )
        former, archive, sha256, blob = record
        assert not (_REPOSITORY_ROOT / former).exists()
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == sha256
        assert _git_blob_id(payload, path=former) == blob
        assert _git_blob_id(payload, path=archive) == blob


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


def test_f06d_satellite_retirement_preserves_exact_residual_boundaries(
    pytestconfig: pytest.Config,
) -> None:
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

    historical_workflow = _assert_f06e_workflow_historical_inventory()
    assert set(_F06D_SATELLITE_PRODUCTION_PATHS) <= historical_workflow.keys()
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
    _assert_f06e_production_archive_payloads(
        _F06E_KERNEL_ARCHIVE_RECORDS, {"kernel": 12}, pytestconfig,
    )
    _assert_f06e_production_archive_payloads(
        _F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS, {"core": 1}, pytestconfig,
        partial_roots=frozenset({"core"}),
    )


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


def test_f06d_core_kernel_retirement_leaves_only_config_containment(
    pytestconfig: pytest.Config,
) -> None:
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
    _assert_f06e_production_archive_payloads(
        _F06E_KERNEL_ARCHIVE_RECORDS, {"kernel": 12}, pytestconfig,
    )
    _assert_f06e_production_archive_payloads(
        _F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS, {"core": 1}, pytestconfig,
        partial_roots=frozenset({"core"}),
    )


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
    *,
    partial_roots: frozenset[str] = frozenset(),
) -> None:
    """Guard an exact archive slice, including explicit leaves of live roots."""

    assert partial_roots <= expected_counts.keys()

    import_suffixes = tuple(importlib.machinery.all_suffixes())
    python_file_patterns = tuple(pytestconfig.getini("python_files"))
    expected_total = sum(expected_counts.values())
    assert len(records) == expected_total
    assert len({record[0] for record in records}) == expected_total
    assert len({record[1] for record in records}) == expected_total

    for root_name, expected_count in expected_counts.items():
        live_root = _REPOSITORY_ROOT / root_name
        if root_name in partial_roots:
            assert live_root.is_dir()
        else:
            assert not live_root.exists()
        root_records = tuple(r for r in records if r[0].startswith(root_name + "/"))
        assert len(root_records) == expected_count
        archive_root = _REPOSITORY_ROOT / "legacy_quarantine/production" / root_name
        if root_name in partial_roots:
            # Each family of a live root owns its exact archived subtree.
            archive_root = Path(os.path.commonpath([
                str((_REPOSITORY_ROOT / record[1]).parent) for record in root_records
            ]))
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
        root_spec = importlib.machinery.PathFinder.find_spec(
            root_name, [str(_REPOSITORY_ROOT)]
        )
        if root_name in partial_roots:
            assert root_spec is not None
        else:
            assert root_spec is None

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
        if root_name in _F06E_DYNAMIC_SATELLITE_PRODUCTION_ROOTS | {"engineering", "workflow"}:
            records = tuple(
                record for record in (
                    _F06E_DYNAMIC_SATELLITE_ARCHIVE_RECORDS
                    + _F06E_ENGINEERING_ARCHIVE_RECORDS
                    + _F06E_WORKFLOW_ARCHIVE_RECORDS
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
    assert legacy_service_consumers == set()
    _assert_f06e_workflow_historical_inventory()
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

_F06E_KERNEL_ARCHIVE_RECORDS = (
    (
        "kernel/__init__.py",
        "legacy_quarantine/production/kernel/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "kernel/boot_manager.py",
        "legacy_quarantine/production/kernel/boot_manager.py.legacy",
        "89f5b35b87f5a5e5dddf1e71417d621da244327f62913e3a535c19ae4fe23b21",
        "46399e1672240c9e6b4252112ddcf92271abb128",
    ),
    (
        "kernel/boot_phase_manager.py",
        "legacy_quarantine/production/kernel/boot_phase_manager.py.legacy",
        "4118d489075afa66085af5166d00b98e5701f66b17b0fa17d1e0f2ab359783b1",
        "d472f5138f243df0fa992834eb2281f92a890ba4",
    ),
    (
        "kernel/jaos_kernel.py",
        "legacy_quarantine/production/kernel/jaos_kernel.py.legacy",
        "9c14d736618909758464687aa8504dfb915f8b246c9c916cb9992ccd2ab54f49",
        "d3aa4c707b77b48bdf8d2d53a4a1eabd88166bea",
    ),
    (
        "kernel/jaos_kernel_backup.py",
        "legacy_quarantine/production/kernel/jaos_kernel_backup.py.legacy",
        "04c634467a013a1a7aba8dd1b66797004077beafb38d2b625f5b0660ca625f26",
        "26cb19d979951c8c13589ac740e7e17142b07dcc",
    ),
    (
        "kernel/kernel_event_bus.py",
        "legacy_quarantine/production/kernel/kernel_event_bus.py.legacy",
        "637eedc0c42c16592588f9e8111b5a78ee35969083fbae6ad0f21c1e0f71ce1c",
        "091db8640403011a38bcb0033da4796504196180",
    ),
    (
        "kernel/kernel_health_monitor.py",
        "legacy_quarantine/production/kernel/kernel_health_monitor.py.legacy",
        "7a0440edfeaac853872a151c8f15ebf9d54de46d49ea5f5f6cbaddc82c44e2b1",
        "b5def8556b47130f1a1c4efdf509ce10c9b8f2ee",
    ),
    (
        "kernel/kernel_lifecycle_manager.py",
        "legacy_quarantine/production/kernel/kernel_lifecycle_manager.py.legacy",
        "8e80ac58805523df6ae4ea16979cb32505394bede15ac3cca82f8f22253cc9e2",
        "cb9af0d1f15140b42bb1badcbb9a78083b07f6ac",
    ),
    (
        "kernel/kernel_permission_gateway.py",
        "legacy_quarantine/production/kernel/kernel_permission_gateway.py.legacy",
        "0cf8d18024bda6e385c91c215f5f772fa2fa6b133e8fba660536ce9e13c6d7c3",
        "8cb8845237e9fa4abe620746f31dc863e85bcd1c",
    ),
    (
        "kernel/kernel_router.py",
        "legacy_quarantine/production/kernel/kernel_router.py.legacy",
        "3dcd6c1deedebe73900b271f53978a634a41ef9ffd7a321bdc57a488b8c4f4c7",
        "893d63d939770b630f2e94f43d930400f2f6d5e1",
    ),
    (
        "kernel/kernel_service_registry.py",
        "legacy_quarantine/production/kernel/kernel_service_registry.py.legacy",
        "a09ef7f7ebb6650255e1e3f0f0e66220adf6dad1f69a60f48206efa20300705a",
        "665e42e331b642ca9ff7f3be4300873af3dda33e",
    ),
    (
        "kernel/runtime_context.py",
        "legacy_quarantine/production/kernel/runtime_context.py.legacy",
        "d3df9aea50620c7f956666be55cf7261edd84d3a727fb917329d3f9b7727d110",
        "f855d6c38c95c3c502bb840bab71902a455f68b8",
    ),
)
_F06E_KERNEL_SOURCE_SIZES = {
    "kernel/__init__.py": 0,
    "kernel/boot_manager.py": 480,
    "kernel/boot_phase_manager.py": 1199,
    "kernel/jaos_kernel.py": 1573,
    "kernel/jaos_kernel_backup.py": 1191,
    "kernel/kernel_event_bus.py": 815,
    "kernel/kernel_health_monitor.py": 1061,
    "kernel/kernel_lifecycle_manager.py": 1235,
    "kernel/kernel_permission_gateway.py": 1040,
    "kernel/kernel_router.py": 882,
    "kernel/kernel_service_registry.py": 628,
    "kernel/runtime_context.py": 945,
}
_F06E_KERNEL_EXCLUDED_IMPORT_STATEMENTS = {
    "tests/boot_manager_test.py": (
        ("kernel.boot_manager",),
    ),
    "tests/boot_phase_manager_test.py": (
        ("kernel.boot_phase_manager",),
    ),
    "tests/jaos_kernel_test.py": (
        ("kernel.jaos_kernel",),
    ),
    "tests/kernel_event_bus_test.py": (
        ("kernel.kernel_event_bus",),
    ),
    "tests/kernel_health_monitor_test.py": (
        ("kernel.kernel_health_monitor",),
    ),
    "tests/kernel_integration_test.py": (
        ("kernel.jaos_kernel",),
        ("kernel.kernel_event_bus",),
        ("kernel.kernel_health_monitor",),
        ("kernel.kernel_lifecycle_manager",),
        ("kernel.kernel_permission_gateway",),
        ("kernel.kernel_router",),
        ("kernel.kernel_service_registry",),
        ("kernel.runtime_context",),
    ),
    "tests/kernel_lifecycle_manager_test.py": (
        ("kernel.kernel_lifecycle_manager",),
    ),
    "tests/kernel_permission_gateway_test.py": (
        ("kernel.kernel_permission_gateway",),
    ),
    "tests/kernel_router_test.py": (
        ("kernel.kernel_router",),
    ),
    "tests/kernel_service_registry_test.py": (
        ("kernel.kernel_service_registry",),
    ),
    "tests/runtime_context_test.py": (
        ("kernel.runtime_context",),
    ),
}
_F06E_KERNEL_EXCLUDED_SCRIPT_HASHES = {
    "tests/boot_manager_test.py":
        "4f9320c4ce4d3d326dd51b141365b7d2ddf00ba00fe8fe4c279c95be7534df9f",
    "tests/boot_phase_manager_test.py":
        "fc207bd6e220a4aad66eb3b1107a10936ccbbbf41d69526d5a14a3d1eaa05573",
    "tests/jaos_kernel_test.py":
        "79e110d8ccce9ca363f211efe3dd060835f265b556b662bd6641560c544ef733",
    "tests/kernel_event_bus_test.py":
        "d1d0ab052ed5d6bdb3d07ddff43bfe84264cd78128dffe308d187855eb7989df",
    "tests/kernel_health_monitor_test.py":
        "00cf0483f80fb4779894e331e427fd5fc3a933f6c52d0737e01d98cbe40dbe87",
    "tests/kernel_integration_test.py":
        "624578db7d3a9473da6debe28685b359371cd84bf8c9714d3d9611cef4b8cf28",
    "tests/kernel_lifecycle_manager_test.py":
        "7e166d7e96a1dd2dacd74e953329d7abe86d8d8d4f6195d16799aec47dc755de",
    "tests/kernel_permission_gateway_test.py":
        "2e51191b74f88f949cb1d2e7a44f4971af673111e0d662aff9a1c7a6ba9bbd5d",
    "tests/kernel_router_test.py":
        "0a573d1f3ff27ca8cae1bb36d100d8e5d3985c1a23b45d9590f6e0a01b99bc76",
    "tests/kernel_service_registry_test.py":
        "5671feffcd9a6ae359cbeb00debaa4e0bb94bc2d9389bdf7bf7d4e2f0349d227",
    "tests/runtime_context_test.py":
        "9de31f72299145893503eb04153b6ae8fa033bfeb1de189dc3238821826c0e07",
}
_F06E_KERNEL_RETAINED_SOURCE_INVENTORIES = {
    "core/kernel.py": (
        1, "2fc94892bf0cff0a3c39e2bce40297c2cee8033150c5dff0aeb39a9256e90f05",
    ),
    "executive_brain": (
        91, "7c75f359f9e8b89a54f4bcc5da6c49a04a6a90845a131da63c15b47a65556cf8",
    ),
    "workflow": (
        9, "0f65197fe64f5eff0753c4277ea8cbf320c19426aa752215bfe6793eb4577d35",
    ),
}


def test_f06e_kernel_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """Preserve all 12 shadow kernel sources outside Python and collection."""

    _assert_f06e_production_archive_payloads(
        _F06E_KERNEL_ARCHIVE_RECORDS, {"kernel": 12}, pytestconfig,
    )
    assert set(_F06E_KERNEL_SOURCE_SIZES) == {
        record[0] for record in _F06E_KERNEL_ARCHIVE_RECORDS
    }
    for former, archive, _sha256, _blob in _F06E_KERNEL_ARCHIVE_RECORDS:
        assert (_REPOSITORY_ROOT / archive).stat().st_size == (
            _F06E_KERNEL_SOURCE_SIZES[former]
        )


def test_f06e_kernel_caller_and_boundary_containment() -> None:
    """Keep exactly the excluded kernel debt and preserve remaining owners."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    paths = _repository_live_python_paths()
    observed: dict[str, tuple[tuple[str, ...], ...]] = {}
    excluded_modules = {
        path.removesuffix(".py").replace("/", ".")
        for path in _F06E_KERNEL_EXCLUDED_IMPORT_STATEMENTS
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
            matching = tuple(name for name in names if name.partition(".")[0] == "kernel")
            if matching:
                statements.append(matching)
            if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names += tuple(node.module + "." + alias.name for alias in node.names)
            assert not any(
                name == module or name.startswith(module + ".")
                for name in names for module in excluded_modules
            ), relpath
            if relpath.startswith(("jaos/", "jaos_platform/")) and (
                isinstance(node, ast.Constant) and isinstance(node.value, str)
            ):
                assert node.value != "kernel"
                assert not node.value.startswith("kernel.")
        if statements:
            observed[relpath] = tuple(statements)
        assert "kernel" not in _literal_dynamic_import_roots(path)

    assert observed == _F06E_KERNEL_EXCLUDED_IMPORT_STATEMENTS
    assert len(observed) == 11
    assert sum(map(len, observed.values())) == 18
    assert all(
        path.startswith("tests/") and not path.startswith("tests/tests/")
        for path in observed
    )
    tests_conftest = _load_tests_conftest()
    assert set(_F06E_KERNEL_EXCLUDED_SCRIPT_HASHES) == set(observed)
    for relpath, expected_sha256 in _F06E_KERNEL_EXCLUDED_SCRIPT_HASHES.items():
        path = _REPOSITORY_ROOT / relpath
        assert tests_conftest.is_excluded_legacy_module(path)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha256

    for relpath, (expected_count, expected_digest) in (
        _F06E_KERNEL_RETAINED_SOURCE_INVENTORIES.items()
    ):
        if relpath == "core/kernel.py":
            former, archive, sha256, blob = _F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS[0]
            assert former == relpath
            assert not (_REPOSITORY_ROOT / former).exists()
            payload = (_REPOSITORY_ROOT / archive).read_bytes()
            assert hashlib.sha256(payload).hexdigest() == sha256
            assert _git_blob_id(payload, path=former) == blob
            assert _git_blob_id(payload, path=archive) == blob
            assert expected_count == 1
            inventory = former + "\0" + sha256 + "\n"
            assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == expected_digest
            continue
        if relpath == "executive_brain":
            _assert_f06e_executive_historical_inventory()
            continue
        if relpath == "workflow":
            _assert_f06e_workflow_historical_inventory()
            continue
        retained = _REPOSITORY_ROOT / relpath
        retained_paths = [retained] if retained.is_file() else sorted(retained.rglob("*.py"))
        assert len(retained_paths) == expected_count
        inventory = "".join(
            path.relative_to(_REPOSITORY_ROOT).as_posix()
            + "\0" + hashlib.sha256(path.read_bytes()).hexdigest() + "\n"
            for path in retained_paths
        )
        assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == expected_digest
    _assert_f06e_satellite_retained_inventory()

    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert "kernel" not in {
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


_F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS = (
    (
        "core/kernel.py",
        "legacy_quarantine/production/core/kernel.py.legacy",
        "12614a613c9156be0dee4aaab6630e161efd04f49b169ce97d27e321086fa86f",
        "7c56418aa60b29dbecaa00f35abeadf70ee65fa9",
    ),
)
_F06E_CORE_KERNEL_REGISTRY_INTERNAL_IMPORTERS = frozenset(
    {
        "executive_brain/brain/executive_brain.py",
        "executive_brain/managers/decision_manager.py",
        "executive_brain/managers/execution_manager.py",
        "executive_brain/managers/mission_manager.py",
        "executive_brain/managers/planning_manager.py",
        "executive_brain/managers/result_manager.py",
    }
)
_F06E_CORE_KERNEL_RETAINED_CORE_DIGEST = (
    "f1b1c574626a8e8c0188f1d8c340cecdf5087eb8e423ad77971a2656a523294c"
)
_F06E_CORE_KERNEL_MAIN_SHA256 = (
    "4194f217f3a896519fed43979407df403a08fdfb3a12fe9d094aef98dba07596"
)


def test_f06e_core_kernel_leaf_archive_preserves_exact_payload(
    pytestconfig: pytest.Config,
) -> None:
    """The one archived leaf is inert while its owning legacy root stays live."""

    _assert_f06e_production_archive_payloads(
        _F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS, {"core": 1}, pytestconfig,
        partial_roots=frozenset({"core"}),
    )
    former, archive, _sha256, _blob = _F06E_CORE_KERNEL_LEAF_ARCHIVE_RECORDS[0]
    payload = (_REPOSITORY_ROOT / archive).read_bytes()
    assert len(payload) == 1888
    assert payload.count(b"\r\n") == 79
    assert payload.count(b"\n") == 79
    assert not tuple((_REPOSITORY_ROOT / "core").rglob("kernel.*.pyc"))
    assert not (_REPOSITORY_ROOT / "core/__pycache__/kernel.cpython-314.pyc").exists()
    assert importlib.machinery.PathFinder.find_spec(
        Path(former).stem, [str(_REPOSITORY_ROOT / "core")]
    ) is None


def test_f06e_core_kernel_leaf_caller_and_dependency_containment() -> None:
    """The leaf stays inert; its six former registry callers are now archived."""

    from tests.tests.platform.test_canonical_import_boundary import (
        _manifest_classified_paths,
        analyze_import_closure,
    )

    leaf = "core.kernel"
    registry = "executive_brain.managers.registry_manager"
    leaf_importers: set[str] = set()
    registry_importers: set[str] = set()
    registry_statement_count = 0
    paths = _repository_live_python_paths()
    for path in paths:
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        package = relpath.removesuffix(".py").replace("/", ".").split(".")[:-1]
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            names: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    prefix = package[:len(package) - node.level + 1]
                    module = ".".join(prefix + ([node.module] if node.module else []))
                else:
                    module = node.module or ""
                names = (module,) + tuple(
                    ".".join(part for part in (module, alias.name) if part)
                    for alias in node.names
                )
            if any(name == leaf or name.startswith(leaf + ".") for name in names):
                leaf_importers.add(relpath)
            if any(name == registry or name.startswith(registry + ".") for name in names):
                registry_importers.add(relpath)
                registry_statement_count += 1
            if isinstance(node, ast.Call) and node.args:
                name = (
                    node.func.id if isinstance(node.func, ast.Name)
                    else node.func.attr if isinstance(node.func, ast.Attribute) else None
                )
                if name in {"import_module", "__import__", "add_import"}:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        assert arg.value != leaf and not arg.value.startswith(leaf + ".")
            if (
                (relpath == "run_jaos.py" or relpath.startswith(("jaos/", "jaos_platform/")))
                and isinstance(node, ast.Constant)
                and isinstance(node.value, str)
            ):
                assert node.value != leaf and not node.value.startswith(leaf + ".")

    # The empty repository-wide set includes production, configured, flat, and tool callers.
    assert leaf_importers == set()
    assert registry_importers == set()
    assert registry_statement_count == 0
    assert all(path.startswith("executive_brain/") for path in registry_importers)

    core = _REPOSITORY_ROOT / "core"
    assert core.is_dir()
    core_sources = sorted(core.rglob("*.py"))
    assert len(core_sources) == 34
    inventory = "".join(
        path.relative_to(_REPOSITORY_ROOT).as_posix() + "\0"
        + hashlib.sha256(path.read_bytes()).hexdigest() + "\n"
        for path in core_sources
    )
    assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == (
        _F06E_CORE_KERNEL_RETAINED_CORE_DIGEST
    )
    assert hashlib.sha256((_REPOSITORY_ROOT / "main.py").read_bytes()).hexdigest() == (
        _F06E_CORE_KERNEL_MAIN_SHA256
    )
    for relpath in ("executive_brain", "workflow"):
        if relpath == "executive_brain":
            _assert_f06e_executive_historical_inventory()
            continue
        assert relpath == "workflow"
        _assert_f06e_workflow_historical_inventory()

    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert leaf not in closure["reached_modules"]
    configured = {
        path for path in paths
        if path.relative_to(_REPOSITORY_ROOT).as_posix().startswith("tests/tests/")
    }
    assert _F06D_CONFIG_CONTAINMENT_PATH in configured
    assert {
        path for path in configured
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    } == {_F06D_CONFIG_CONTAINMENT_PATH}
    assert not any(
        "executive_brain" in _imported_top_level_roots(path) for path in configured
    )
    _assert_config_containment_preserved()

    manifest = (
        _REPOSITORY_ROOT / "docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md"
    ).read_text(encoding="utf-8")
    classified = _manifest_classified_paths(manifest)
    assert "core/" in classified["D"]
    assert "legacy_quarantine/production/core/kernel.py.legacy" not in classified["E"]
    assert {code: len(entries) for code, entries in classified.items()} == {
        "A": 10, "B": 1, "D": 4, "E": 15, "F": 3,
    }
    assert sum(map(len, classified.values())) == 33

_F06E_EXECUTIVE_AI_ARCHIVE_RECORDS = (
    (
        "executive_brain/ai/__init__.py",
        "legacy_quarantine/production/executive_brain/ai/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "executive_brain/ai/prompt/__init__.py",
        "legacy_quarantine/production/executive_brain/ai/prompt/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "executive_brain/ai/prompt/prompt_engine.py",
        "legacy_quarantine/production/executive_brain/ai/prompt/prompt_engine.py.legacy",
        "1424acfe1dd56b959cb848ed9e986235c02e8b353a906e2a931b9d0e303bac51",
        "c8d2e25717e88b244ce4d77421ad4f559313663f",
    ),
    (
        "executive_brain/ai/prompt/prompt_models.py",
        "legacy_quarantine/production/executive_brain/ai/prompt/prompt_models.py.legacy",
        "11f8f8293b3af59c7175570ce507b1ace1aa2616506f870f4979c2c2ddc5381a",
        "3c83332640dd4caff851095d60a5d4e415518782",
    ),
    (
        "executive_brain/ai/providers/__init__.py",
        "legacy_quarantine/production/executive_brain/ai/providers/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "executive_brain/ai/providers/ai_provider_exceptions.py",
        "legacy_quarantine/production/executive_brain/ai/providers/ai_provider_exceptions.py.legacy",
        "09ed65a45fbbe6ee965b09ae1f9c167af5acb88bfbd7f52083d062cd1d2a1e72",
        "b048a757e8ad282194096ba6aa609415524c392a",
    ),
    (
        "executive_brain/ai/providers/ai_provider_interface.py",
        "legacy_quarantine/production/executive_brain/ai/providers/ai_provider_interface.py.legacy",
        "fa6d2d0b6bb453c0189b840573d4957e5e284e2f6f3d6c5c431a37c30128a5d3",
        "c6ba37a7809bd51fc549f4aa87ac465c75fb23cb",
    ),
    (
        "executive_brain/ai/providers/ai_provider_manager.py",
        "legacy_quarantine/production/executive_brain/ai/providers/ai_provider_manager.py.legacy",
        "7f1125e41a5379e42daffc7d9bd360ad2e0f0db09a4a390c17781b257c7a0618",
        "c1b2ca6103c352aaab8f6748cac1dc9116e8e13a",
    ),
    (
        "executive_brain/ai/providers/ai_provider_models.py",
        "legacy_quarantine/production/executive_brain/ai/providers/ai_provider_models.py.legacy",
        "5b3e4011f8350c8a7dcee9069c9681bab3f694af5c3464c09bb2a85fba1fee54",
        "6810938055892b0e72f09473f481b520c73ad1eb",
    ),
    (
        "executive_brain/ai/providers/ollama_provider.py",
        "legacy_quarantine/production/executive_brain/ai/providers/ollama_provider.py.legacy",
        "51a18d7db6c99646f5905a617b6b8f11543d2f2037de8ea504d0c24aaf46cbb0",
        "95144406d1b48487f7af6ebf82c6f5ca80653261",
    ),
    (
        "executive_brain/ai/providers/openai_provider.py",
        "legacy_quarantine/production/executive_brain/ai/providers/openai_provider.py.legacy",
        "c1a42f8585db3edc84b26735eb4b41e7680ff8a58531596bb608dcf67a10596d",
        "bfb0ee10589c054903e214d69285afb8dc8a242f",
    ),
    (
        "executive_brain/ai/routing/__init__.py",
        "legacy_quarantine/production/executive_brain/ai/routing/__init__.py.legacy",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    ),
    (
        "executive_brain/ai/routing/llm_router.py",
        "legacy_quarantine/production/executive_brain/ai/routing/llm_router.py.legacy",
        "e166501f63aad131377883964664efdf8a2ba30a23d9bcb445f053be1e7305e4",
        "cd46a08e075da86f10a9002337b4cc8f474a2349",
    ),
)
_F06E_EXECUTIVE_AI_SOURCE_SIZES_AND_CRLF = {
    "executive_brain/ai/__init__.py": (0, 0),
    "executive_brain/ai/prompt/__init__.py": (0, 0),
    "executive_brain/ai/prompt/prompt_engine.py": (2276, 73),
    "executive_brain/ai/prompt/prompt_models.py": (883, 50),
    "executive_brain/ai/providers/__init__.py": (0, 0),
    "executive_brain/ai/providers/ai_provider_exceptions.py": (495, 24),
    "executive_brain/ai/providers/ai_provider_interface.py": (1046, 48),
    "executive_brain/ai/providers/ai_provider_manager.py": (2920, 87),
    "executive_brain/ai/providers/ai_provider_models.py": (1028, 47),
    "executive_brain/ai/providers/ollama_provider.py": (3763, 131),
    "executive_brain/ai/providers/openai_provider.py": (4236, 146),
    "executive_brain/ai/routing/__init__.py": (0, 0),
    "executive_brain/ai/routing/llm_router.py": (1337, 46),
}
_F06E_EXECUTIVE_AI_RETAINED_INVENTORIES = {
    "executive_brain": (
        78, "84cf9864b24778fbb43d8bd7382fe8ed62eaabe79083bebd83a661f3de274533",
    ),
    "executive_brain/tools": (
        42, "67f6d96cedf6a61124cddbd1e14f4fe0eb08a7392adc3621e2e76982bbede625",
    ),
    "workflow": (
        9, "0f65197fe64f5eff0753c4277ea8cbf320c19426aa752215bfe6793eb4577d35",
    ),
}


def _assert_f06e_executive_historical_inventory() -> dict[str, bytes]:
    """Reconstruct the original 91-file evidence from live and archived bytes."""

    payloads = {
        path.relative_to(_REPOSITORY_ROOT).as_posix(): path.read_bytes()
        for path in (_REPOSITORY_ROOT / "executive_brain").rglob("*.py")
    }
    assert payloads == {}
    for former, archive, sha256, blob in (
        *_F06E_EXECUTIVE_AI_ARCHIVE_RECORDS,
        *_F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS,
        *_F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS,
    ):
        assert former not in payloads
        assert not (_REPOSITORY_ROOT / former).exists()
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == sha256
        assert _git_blob_id(payload, path=former) == blob
        payloads[former] = payload
    expected_count, expected_digest = _F06E_KERNEL_RETAINED_SOURCE_INVENTORIES[
        "executive_brain"
    ]
    assert len(payloads) == expected_count == 91
    inventory = "".join(
        relpath + "\0" + hashlib.sha256(payload).hexdigest() + "\n"
        for relpath, payload in sorted(payloads.items())
    )
    assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == expected_digest
    return payloads


def test_f06e_executive_ai_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """The exact 13-source partial-root slice is inert and byte-identical."""

    _assert_f06e_production_archive_payloads(
        _F06E_EXECUTIVE_ALL_ARCHIVE_RECORDS, {"executive_brain": 91}, pytestconfig,
    )
    family = _REPOSITORY_ROOT / "executive_brain/ai"
    assert not family.exists()
    for relative in ("__pycache__", "prompt/__pycache__", "providers/__pycache__",
                     "routing/__pycache__"):
        assert not (family / relative).exists()
    assert importlib.machinery.PathFinder.find_spec(
        "ai", [str(family.parent)]
    ) is None
    assert set(_F06E_EXECUTIVE_AI_SOURCE_SIZES_AND_CRLF) == {
        record[0] for record in _F06E_EXECUTIVE_AI_ARCHIVE_RECORDS
    }
    for former, archive, _sha256, _blob in _F06E_EXECUTIVE_AI_ARCHIVE_RECORDS:
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        size, crlf = _F06E_EXECUTIVE_AI_SOURCE_SIZES_AND_CRLF[former]
        assert len(payload) == size
        assert payload.count(b"\r\n") == payload.count(b"\n") == crlf
        assert payload.count(b"\r") == crlf


def _assert_f06e_executive_family_caller_containment(family: str) -> None:
    """Reuse the Executive AST boundary guard without executing retired code."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    registry = "executive_brain.managers.registry_manager"
    callers: set[str] = set()
    registry_importers: set[str] = set()
    registry_statements = 0
    workflow_edges: set[str] = set()
    paths = _repository_live_python_paths()
    for path in paths:
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        package = relpath.removesuffix(".py").replace("/", ".").split(".")[:-1]
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
            names: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                prefix = package[:len(package) - node.level + 1] if node.level else []
                module = ".".join(prefix + ([node.module] if node.module else []))
                names = (module,) + tuple(
                    ".".join(part for part in (module, alias.name) if part)
                    for alias in node.names
                )
            elif isinstance(node, ast.Call) and node.args:
                function = (
                    node.func.id if isinstance(node.func, ast.Name)
                    else node.func.attr if isinstance(node.func, ast.Attribute) else None
                )
                argument = node.args[0]
                if (
                    function in {"import_module", "__import__", "add_import"}
                    and isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                ):
                    names = (argument.value,)
            if any(name == family or name.startswith(family + ".") for name in names):
                callers.add(relpath)
            assert not any(
                name == "legacy_quarantine" or name.startswith("legacy_quarantine.")
                for name in names
            )
            if any(name == registry or name.startswith(registry + ".") for name in names):
                registry_importers.add(relpath)
                registry_statements += 1
            if "workflow.workflow_engine" in names:
                workflow_edges.add(relpath)
            # Dotted lazy-map targets are imports; explanatory inventory prose is not.
            if (
                (relpath == "run_jaos.py" or relpath.startswith(("jaos/", "jaos_platform/")))
                and isinstance(node, ast.Constant) and isinstance(node.value, str)
                and all(part.isidentifier() for part in node.value.split("."))
            ):
                assert node.value != family and not node.value.startswith(family + ".")

    # This repository-wide empty set includes configured, excluded, and tool callers.
    assert callers == set()
    assert registry_importers == set()
    assert registry_statements == 0
    assert not {p for p in workflow_edges if not p.startswith("tests/")}
    assert all(path.startswith("executive_brain/") for path in registry_importers)
    historical = _assert_f06e_executive_historical_inventory()
    for root, (count, digest) in _F06E_EXECUTIVE_AI_RETAINED_INVENTORIES.items():
        if root.startswith("executive_brain"):
            payloads = {
                relpath: payload for relpath, payload in historical.items()
                if relpath.startswith(root + "/")
                and not relpath.startswith("executive_brain/ai/")
            }
        else:
            assert root == "workflow"
            payloads = _assert_f06e_workflow_historical_inventory()
        assert len(payloads) == count
        inventory = "".join(
            relpath + "\0" + hashlib.sha256(payload).hexdigest() + "\n"
            for relpath, payload in sorted(payloads.items())
        )
        assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == digest
    executive = _REPOSITORY_ROOT / "executive_brain"
    assert not executive.exists()
    assert not tuple(executive.rglob("*.py"))
    assert not (executive / "tools").exists()

    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert closure["analyzed_files"]
    assert not any(
        module == family or module.startswith(family + ".")
        for module in closure["reached_modules"]
    )
    configured = {
        path for path in paths
        if path.relative_to(_REPOSITORY_ROOT).as_posix().startswith("tests/tests/")
    }
    assert {
        path for path in configured
        if _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
    } == {_F06D_CONFIG_CONTAINMENT_PATH}
    assert not any("executive_brain" in _imported_top_level_roots(p) for p in configured)
    _assert_config_containment_preserved()


def test_f06e_executive_ai_caller_provider_and_dependency_containment() -> None:
    """AI retirement still preserves provider contracts after tools retirement."""

    from tests.tests.platform.test_canonical_import_boundary import (
        _manifest_classified_paths,
    )

    _assert_f06e_executive_family_caller_containment("executive_brain.ai")
    adr = (_REPOSITORY_ROOT / "docs/architecture/ARCHITECTURE_DECISIONS.md").read_text(
        encoding="utf-8"
    ).split("\\# ADR-0014", 1)[1].split("\\# Review Policy", 1)[0]
    for evidence in (
        "ACCEPTED", "Founder-approved 2026-08-31",
        "exact legacy OpenAI and Ollama adapters", "shadow\narchitecture",
        "not permanent JAOS provider contracts", "No OpenAI-specific or Ollama-specific",
        "`ProviderManager`/`AIManager`", "`MockProvider`",
        "FORTRESS-09 remains NOT STARTED", "FORTRESS-09 retains later",
    ):
        assert evidence in adr
    provider_architecture = (
        _REPOSITORY_ROOT / "docs/architecture/PROVIDER_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    assert "ADR-0014 supersedes" in provider_architecture
    assert _F06D_PROVIDER_CANONICAL_TEST_PATH.is_file()
    assert _imported_top_level_roots(_F06D_PROVIDER_CANONICAL_TEST_PATH) == {"jaos", "pytest"}
    manifest = (
        _REPOSITORY_ROOT / "docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md"
    ).read_text(encoding="utf-8")
    classified = _manifest_classified_paths(manifest)
    assert "legacy_quarantine/production/executive_brain/" in classified["E"]
    assert not any("executive_brain/ai" in entry for entry in classified["E"])
    assert {code: len(entries) for code, entries in classified.items()} == {
        "A": 10, "B": 1, "D": 4, "E": 15, "F": 3,
    }
    assert sum(map(len, classified.values())) == 33


_F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS = (
    (
        'executive_brain/tools/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/browser/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/browser/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/browser/browser_automation_tool.py',
        'legacy_quarantine/production/executive_brain/tools/browser/browser_automation_tool.py.legacy',
        '94625edd3f8c190642bfea5cf0c328fdc0a86411de5b2f2969f4409266a567e7',
        '2e3c19713edbf0959b06c53bc28069f526a9f408',
    ),
    (
        'executive_brain/tools/browser/browser_exceptions.py',
        'legacy_quarantine/production/executive_brain/tools/browser/browser_exceptions.py.legacy',
        '2c52f39e26cc50d97f1321d70da839545dec86e2fa681f55b9cf29bc689f23f4',
        '0fd188159229f457af49e095e4437c12df22cd11',
    ),
    (
        'executive_brain/tools/browser/browser_interface.py',
        'legacy_quarantine/production/executive_brain/tools/browser/browser_interface.py.legacy',
        '3e1aad93e8ff6f4e7f67562bd714e01941f49629fd0a8a9cde32157ee55a4109',
        '6d2ec19432df7f648de01dfb633d5c88c199c3fd',
    ),
    (
        'executive_brain/tools/browser/browser_manager.py',
        'legacy_quarantine/production/executive_brain/tools/browser/browser_manager.py.legacy',
        '9c4fc7a34891cd58593aeee2701e6eaab19c908389250f2f635d03d1a3059e88',
        '88921d49c88e5c4eb8dac4f35158f96619bfc336',
    ),
    (
        'executive_brain/tools/browser/browser_models.py',
        'legacy_quarantine/production/executive_brain/tools/browser/browser_models.py.legacy',
        'c4a5e762e6b2f306a2abebfe372e905e3325d729dc54867fa660acaee7724c6d',
        'a230257f2a4ab6f794172b70a19aceeb69fe2c70',
    ),
    (
        'executive_brain/tools/browser/cookies_tool.py',
        'legacy_quarantine/production/executive_brain/tools/browser/cookies_tool.py.legacy',
        'c5b1dc692ac7afc563c32734c4fdcf2cc4981e29ca6dc4978d08df49ec87f10e',
        'cf67977d8be064a8aec3ca42a80c722464731e68',
    ),
    (
        'executive_brain/tools/browser/downloads_tool.py',
        'legacy_quarantine/production/executive_brain/tools/browser/downloads_tool.py.legacy',
        '0ba872af8c97367b7dc43f8a237f9a765c0105a41009fa1a3858aa139708f0c9',
        '8a9db1f72a826ea9109c70c0b3b22ffb14e0f1f5',
    ),
    (
        'executive_brain/tools/browser/tabs_tool.py',
        'legacy_quarantine/production/executive_brain/tools/browser/tabs_tool.py.legacy',
        '094694c808538bc4304ca70e33ce7d1ca1aaf71fa481b235cb344f309fbdc066',
        '3bfcb920891f08490605e31c2f090f24367b583e',
    ),
    (
        'executive_brain/tools/browser/web_search_tool.py',
        'legacy_quarantine/production/executive_brain/tools/browser/web_search_tool.py.legacy',
        '2194b4a2381297a1d1e2b61189757c489d01075fd801e3b916926fd1c62f1904',
        'de1ed10efeecc1e315c0dd17b3683de180ca10b4',
    ),
    (
        'executive_brain/tools/core/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/core/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/core/tool_exceptions.py',
        'legacy_quarantine/production/executive_brain/tools/core/tool_exceptions.py.legacy',
        'b987ce63de86442b9eeef4440e51edff7d9c4b4e485cc58ff66f4cdc41262441',
        'f4f41abd6a00e40b8f19840299d7963246df7e3b',
    ),
    (
        'executive_brain/tools/core/tool_interface.py',
        'legacy_quarantine/production/executive_brain/tools/core/tool_interface.py.legacy',
        '55984992fea16fb9ca09d7838225dc271c20fb309d51319833a7e487a31d1ce6',
        'e2958718da6db818dec67b39cee4b374722c89e4',
    ),
    (
        'executive_brain/tools/core/tool_manager.py',
        'legacy_quarantine/production/executive_brain/tools/core/tool_manager.py.legacy',
        '39d431f7bdad18539d28ee5f55e28fcad3a7e291865c40992d0418d9334107a7',
        '158af932d819d82574e484c975692b1b2247afbe',
    ),
    (
        'executive_brain/tools/core/tool_models.py',
        'legacy_quarantine/production/executive_brain/tools/core/tool_models.py.legacy',
        '5cbbd91e926b62e272a5512604b681569cfaa9750f7c26242c821ebb274b3e7a',
        '0b7eb1bc0a7cb3faff4dfdfd2a9fd66c61d3f74c',
    ),
    (
        'executive_brain/tools/core/tool_registry.py',
        'legacy_quarantine/production/executive_brain/tools/core/tool_registry.py.legacy',
        '2f36bcc4da3264667ad4c3d98660a911d115eb9c1859c8bd8a81e74070ffa000',
        'f975f4d13ce59d91536b5971b0282757bd8d2f46',
    ),
    (
        'executive_brain/tools/development/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/development/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/development/ide_exceptions.py',
        'legacy_quarantine/production/executive_brain/tools/development/ide_exceptions.py.legacy',
        '66864cd78449d61948e2335f164b384054356204afb9bcb83f43bd64653b1582',
        '4d6fe467f159abc75fed471bf5d7103d4cf23c64',
    ),
    (
        'executive_brain/tools/development/ide_interface.py',
        'legacy_quarantine/production/executive_brain/tools/development/ide_interface.py.legacy',
        'af0f2c4defa9e39c606426cde68901dcbe10f9746de64dc40912f795453f9059',
        'b329312b490422437de071c11f6ee54943a13a9a',
    ),
    (
        'executive_brain/tools/development/ide_manager.py',
        'legacy_quarantine/production/executive_brain/tools/development/ide_manager.py.legacy',
        '9e5c5d05c34f83e2a787af8f5c7f7775e29cee09d4d54bedf4f2db6a69e194cb',
        '7334058d11ef3906fd8b1450b270bf70785bc3b2',
    ),
    (
        'executive_brain/tools/development/ide_models.py',
        'legacy_quarantine/production/executive_brain/tools/development/ide_models.py.legacy',
        '9f0ef34d04fe91845d1fab1c2d7f75ef2d0d4e1a064d984800a53fa949c4f8c4',
        '2c1abc6775a46a9969f748cb9c94ce48fcc10acc',
    ),
    (
        'executive_brain/tools/development/vscode/build_tool.py',
        'legacy_quarantine/production/executive_brain/tools/development/vscode/build_tool.py.legacy',
        'f4ab7ab8484d44c57aba2b863167714f37dd2a2fb996aa5332e217083bf344fd',
        '522502abb21161765b65599a5a5ec28d028c75de',
    ),
    (
        'executive_brain/tools/development/vscode/debug_tool.py',
        'legacy_quarantine/production/executive_brain/tools/development/vscode/debug_tool.py.legacy',
        '6c81cdb86c9b08a8ccf5c933d1a5f4c8fcaf49c314542decfa9885f234a2a05d',
        '7d6e1a2acf0e467484fbca433c322c81a13d86e7',
    ),
    (
        'executive_brain/tools/development/vscode/git_tool.py',
        'legacy_quarantine/production/executive_brain/tools/development/vscode/git_tool.py.legacy',
        '2becf449a18dfc9d697e1d2c6f101389b7f1c97b866ebd2049b1e1d0e24d5553',
        '0d071742e785daa15ad147127f7cb739406535ef',
    ),
    (
        'executive_brain/tools/development/vscode/project_tool.py',
        'legacy_quarantine/production/executive_brain/tools/development/vscode/project_tool.py.legacy',
        '382a761e3082bef712a6bca97479bb25b2a65a766995ba4599ca5d8d95719aaa',
        '9239cbafc2400ab29df1a73bf7f57f3399106da2',
    ),
    (
        'executive_brain/tools/development/vscode/run_tool.py',
        'legacy_quarantine/production/executive_brain/tools/development/vscode/run_tool.py.legacy',
        'ecac46d4c53114edffa3c13d04036ff30831c3a49f8aff821706045c1afde368',
        'b754cc86e22c68a43f0c33aa390ab733e211a731',
    ),
    (
        'executive_brain/tools/file/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/file/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/file/copy_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/copy_file_tool.py.legacy',
        '3e644c8d0f8fc69bce098f5b05307541d7591a2614b12bf43087b9d9b04b8ed8',
        '0ec0339b0d02541c4b984a1fd058794e6e9fffc8',
    ),
    (
        'executive_brain/tools/file/delete_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/delete_file_tool.py.legacy',
        '8ffcd9bb4d1fdb8ff3da76d7232090796b860b7b7be627d93b07f94dbdd0c386',
        '0e41a1bebc50dbcc0cb5e2e41d00d7cbdb2bce7f',
    ),
    (
        'executive_brain/tools/file/move_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/move_file_tool.py.legacy',
        '3d82c2503a95a13bdc10a279124938ab7ab2b627d1d4679ceb9b73ebfe36943b',
        '13f078ecfd4d87764f89e26e77789ce531d1e24a',
    ),
    (
        'executive_brain/tools/file/read_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/read_file_tool.py.legacy',
        '39fc62167618107278d7aa09edf0518b88a10891d2a6da174b6eb874611967c9',
        'cf97c669c661a62223534d479a5e616f96723b9b',
    ),
    (
        'executive_brain/tools/file/rename_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/rename_file_tool.py.legacy',
        'bd5a07b2ded36955d922e2a612d823d4a8199ad8c7756dc89c3d3d5b35682734',
        'd2cab21e55b8c1f3ff69c4d9381f4b38f0ed6e65',
    ),
    (
        'executive_brain/tools/file/search_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/search_file_tool.py.legacy',
        '77aa69e3e998dc225babfb3cad4279299e10dfa264c5a20614ea8ce544a5d551',
        '826cc9a938d01a9146b562ec30c2e681e578f525',
    ),
    (
        'executive_brain/tools/file/write_file_tool.py',
        'legacy_quarantine/production/executive_brain/tools/file/write_file_tool.py.legacy',
        '915de2957409dbd5968fbdbf175653711fb7ef238f580a10ebc681bae05be61c',
        '39e9c76a4b66687cdff61c175f7d2590a792e030',
    ),
    (
        'executive_brain/tools/windows/__init__.py',
        'legacy_quarantine/production/executive_brain/tools/windows/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/tools/windows/clipboard_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/clipboard_tool.py.legacy',
        'ed5e7daa97eb65d7b6c22c253215748157dda40d64e0043723197126b48eb652',
        '1c5369dd46a49a732fc0183117f62e0a7b869d03',
    ),
    (
        'executive_brain/tools/windows/close_application_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/close_application_tool.py.legacy',
        '71c21a6f2a5e7fe62d97d76d11b58626a89c5f96965a36c062494d9f7388070f',
        'e1823dd8db67c3dd42f5e7aed8b1a47cfd541425',
    ),
    (
        'executive_brain/tools/windows/launch_application_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/launch_application_tool.py.legacy',
        '3f7cccfc69d21588f35829e457e26108b9037cc006c5282feee3cce49a1421d6',
        '72c915b16bb153321ef972c4b8ad4b7d6aa5fbbf',
    ),
    (
        'executive_brain/tools/windows/notification_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/notification_tool.py.legacy',
        '6c0d45dd795c73ac24de914592e4504d2c2a31e883e2563a4e2eac534ac301ca',
        'c2d27f11f73555d4f29eeede9c21c7365a6d45c9',
    ),
    (
        'executive_brain/tools/windows/process_manager_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/process_manager_tool.py.legacy',
        'a9a83584fa37ffff623fd6b68b2bd7211488647f0839563fa1ac24f39749266a',
        '321048b0fed43b7c9aca6884f4bd69162b4ecef0',
    ),
    (
        'executive_brain/tools/windows/services_tool.py',
        'legacy_quarantine/production/executive_brain/tools/windows/services_tool.py.legacy',
        'ae661a81f5068938d082d1a08699f3f6d20acfedc7fef7336efc01b77c970287',
        'a93dae3232c0c6f3d18124d5906daa23e444acf4',
    ),
)
_F06E_EXECUTIVE_TOOLS_SOURCE_SIZES_AND_CRLF = {
    'executive_brain/tools/__init__.py': (0, 0),
    'executive_brain/tools/browser/__init__.py': (0, 0),
    'executive_brain/tools/browser/browser_automation_tool.py': (1370, 55),
    'executive_brain/tools/browser/browser_exceptions.py': (448, 24),
    'executive_brain/tools/browser/browser_interface.py': (962, 44),
    'executive_brain/tools/browser/browser_manager.py': (1577, 55),
    'executive_brain/tools/browser/browser_models.py': (753, 41),
    'executive_brain/tools/browser/cookies_tool.py': (1562, 56),
    'executive_brain/tools/browser/downloads_tool.py': (2025, 74),
    'executive_brain/tools/browser/tabs_tool.py': (1261, 51),
    'executive_brain/tools/browser/web_search_tool.py': (2543, 85),
    'executive_brain/tools/core/__init__.py': (0, 0),
    'executive_brain/tools/core/tool_exceptions.py': (433, 24),
    'executive_brain/tools/core/tool_interface.py': (740, 36),
    'executive_brain/tools/core/tool_manager.py': (1813, 69),
    'executive_brain/tools/core/tool_models.py': (689, 41),
    'executive_brain/tools/core/tool_registry.py': (1937, 79),
    'executive_brain/tools/development/__init__.py': (0, 0),
    'executive_brain/tools/development/ide_exceptions.py': (419, 24),
    'executive_brain/tools/development/ide_interface.py': (918, 44),
    'executive_brain/tools/development/ide_manager.py': (1498, 55),
    'executive_brain/tools/development/ide_models.py': (728, 41),
    'executive_brain/tools/development/vscode/build_tool.py': (2491, 85),
    'executive_brain/tools/development/vscode/debug_tool.py': (2491, 85),
    'executive_brain/tools/development/vscode/git_tool.py': (2531, 85),
    'executive_brain/tools/development/vscode/project_tool.py': (1829, 69),
    'executive_brain/tools/development/vscode/run_tool.py': (2475, 85),
    'executive_brain/tools/file/__init__.py': (0, 0),
    'executive_brain/tools/file/copy_file_tool.py': (1807, 64),
    'executive_brain/tools/file/delete_file_tool.py': (1560, 60),
    'executive_brain/tools/file/move_file_tool.py': (1813, 64),
    'executive_brain/tools/file/read_file_tool.py': (1670, 63),
    'executive_brain/tools/file/rename_file_tool.py': (1763, 62),
    'executive_brain/tools/file/search_file_tool.py': (2002, 72),
    'executive_brain/tools/file/write_file_tool.py': (1449, 54),
    'executive_brain/tools/windows/__init__.py': (0, 0),
    'executive_brain/tools/windows/clipboard_tool.py': (1134, 50),
    'executive_brain/tools/windows/close_application_tool.py': (1421, 56),
    'executive_brain/tools/windows/launch_application_tool.py': (2306, 76),
    'executive_brain/tools/windows/notification_tool.py': (1725, 65),
    'executive_brain/tools/windows/process_manager_tool.py': (2540, 95),
    'executive_brain/tools/windows/services_tool.py': (2843, 98),
}
_F06E_EXECUTIVE_TOOLS_REMAINING_SOURCES = (
    'executive_brain/__init__.py',
    'executive_brain/brain/__init__.py',
    'executive_brain/brain/executive_brain.py',
    'executive_brain/common/__init__.py',
    'executive_brain/common/enums.py',
    'executive_brain/intent.py',
    'executive_brain/managers/__init__.py',
    'executive_brain/managers/decision_manager.py',
    'executive_brain/managers/execution_manager.py',
    'executive_brain/managers/mission_manager.py',
    'executive_brain/managers/planning_manager.py',
    'executive_brain/managers/registry_manager.py',
    'executive_brain/managers/result_manager.py',
    'executive_brain/memory/__init__.py',
    'executive_brain/memory/memory_manager.py',
    'executive_brain/memory/memory_registry.py',
    'executive_brain/memory/working_memory.py',
    'executive_brain/models/__init__.py',
    'executive_brain/models/context_snapshot_model.py',
    'executive_brain/models/decision_model.py',
    'executive_brain/models/execution_plan_model.py',
    'executive_brain/models/goal_model.py',
    'executive_brain/models/intent_model.py',
    'executive_brain/models/mission_model.py',
    'executive_brain/models/result_model.py',
    'executive_brain/pipeline/executive_pipeline.py',
    'executive_brain/planner/__init__.py',
    'executive_brain/registries/__init__.py',
    'executive_brain/registries/base_registry.py',
    'executive_brain/registries/decision_registry.py',
    'executive_brain/registries/execution_plan_registry.py',
    'executive_brain/registries/goal_registry.py',
    'executive_brain/registries/intent_registry.py',
    'executive_brain/registries/mission_registry.py',
    'executive_brain/registries/result_registry.py',
    'executive_brain/timeline/__init__.py',
)


def test_f06e_executive_tools_archives_preserve_exact_payloads(
    pytestconfig: pytest.Config,
) -> None:
    """The exact 42-source family is inert, byte-identical and non-collectable."""

    _assert_f06e_production_archive_payloads(
        _F06E_EXECUTIVE_ALL_ARCHIVE_RECORDS, {"executive_brain": 91}, pytestconfig,
    )
    family = _REPOSITORY_ROOT / "executive_brain/tools"
    assert not family.exists()
    for relative in (
        "__pycache__", "browser/__pycache__", "core/__pycache__",
        "development/__pycache__", "development/vscode/__pycache__",
        "file/__pycache__", "windows/__pycache__",
    ):
        assert not (family / relative).exists()
    assert importlib.machinery.PathFinder.find_spec("tools", [str(family.parent)]) is None
    assert set(_F06E_EXECUTIVE_TOOLS_SOURCE_SIZES_AND_CRLF) == {
        record[0] for record in _F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS
    }
    for former, archive, _sha256, _blob in _F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS:
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        size, crlf = _F06E_EXECUTIVE_TOOLS_SOURCE_SIZES_AND_CRLF[former]
        assert len(payload) == size
        assert payload.count(b"\r\n") == payload.count(b"\n") == crlf
        assert payload.count(b"\r") == crlf
    _assert_f06e_executive_historical_inventory()


def test_f06e_executive_tools_caller_effect_and_dependency_containment() -> None:
    """Zero callers and preserved canonical owners need no legacy execution."""

    from tests.tests.platform.test_canonical_import_boundary import (
        _manifest_classified_paths,
    )

    _assert_f06e_executive_family_caller_containment("executive_brain.tools")
    # Inspect archive ASTs only; importing these capabilities is never required.
    internal_statements = 0
    internal_consumers: set[str] = set()
    effect_calls: dict[str, set[str]] = {}
    for former, archive, _sha256, _blob in _F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS:
        tree = ast.parse((_REPOSITORY_ROOT / archive).read_text(encoding="utf-8-sig"))
        effect_calls[former] = {
            ast.unparse(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith("executive_brain."):
                    assert node.module.startswith("executive_brain.tools.")
                    internal_statements += 1
                    internal_consumers.add(former)
            elif isinstance(node, ast.Import):
                assert not any(alias.name.startswith("executive_brain") for alias in node.names)
    assert internal_statements == 57
    assert len(internal_consumers) == 30
    for relative, call in (
        ("browser/browser_automation_tool.py", "webbrowser.open"),
        ("browser/downloads_tool.py", "webbrowser.open"),
        ("browser/tabs_tool.py", "webbrowser.open_new_tab"),
        ("browser/web_search_tool.py", "webbrowser.open"),
        ("browser/cookies_tool.py", "path.exists"),
        ("development/vscode/build_tool.py", "subprocess.run"),
        ("development/vscode/debug_tool.py", "subprocess.run"),
        ("development/vscode/git_tool.py", "subprocess.run"),
        ("development/vscode/project_tool.py", "subprocess.Popen"),
        ("development/vscode/run_tool.py", "subprocess.run"),
        ("file/copy_file_tool.py", "shutil.copy2"),
        ("file/delete_file_tool.py", "file_path.unlink"),
        ("file/move_file_tool.py", "shutil.move"),
        ("file/read_file_tool.py", "file_path.read_text"),
        ("file/rename_file_tool.py", "source_path.rename"),
        ("file/search_file_tool.py", "root.rglob"),
        ("file/write_file_tool.py", "file_path.write_text"),
        ("windows/clipboard_tool.py", "root.clipboard_get"),
        ("windows/close_application_tool.py", "os.kill"),
        ("windows/launch_application_tool.py", "subprocess.Popen"),
        ("windows/notification_tool.py", "ctypes.windll.user32.MessageBoxW"),
        ("windows/process_manager_tool.py", "subprocess.run"),
        ("windows/services_tool.py", "subprocess.run"),
    ):
        assert call in effect_calls["executive_brain/tools/" + relative]

    # Canonical ownership is verified structurally here and behaviorally by its
    # configured Tool Platform tests; F07/F11 policy is not extended by this slice.
    composition = _REPOSITORY_ROOT / "jaos/composition/platform_composition.py"
    tree = ast.parse(composition.read_text(encoding="utf-8"))
    assert any(
        isinstance(node, ast.ImportFrom) and node.module == "jaos.tools.tool_manager"
        and any(alias.name == "ToolManager" for alias in node.names)
        for node in ast.walk(tree)
    )
    assert "executive_brain" not in _imported_top_level_roots(composition)
    for relative in (
        "jaos/tools/tool_manager.py", "jaos/tools/tool_registry.py",
        "jaos/tools/tool_execution.py", "jaos/tools/tool_permissions.py",
        "jaos/tools/tool_approval.py", "jaos/tools/tool_audit.py",
    ):
        assert (_REPOSITORY_ROOT / relative).is_file()
    manifest = (
        _REPOSITORY_ROOT / "docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md"
    ).read_text(encoding="utf-8")
    classified = _manifest_classified_paths(manifest)
    assert classified["D"] == {
        "brain/", "core/", "main.py", "memory/",
    }
    assert not any("executive_brain/tools" in entry for entry in classified["E"])
    assert {code: len(entries) for code, entries in classified.items()} == {
        "A": 10, "B": 1, "D": 4, "E": 15, "F": 3,
    }
    assert sum(map(len, classified.values())) == 33


# Final root-family evidence captured at b0c2e1e before the atomic move.
_F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS = (
    (
        'executive_brain/__init__.py',
        'legacy_quarantine/production/executive_brain/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/brain/__init__.py',
        'legacy_quarantine/production/executive_brain/brain/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/brain/executive_brain.py',
        'legacy_quarantine/production/executive_brain/brain/executive_brain.py.legacy',
        'b3b6764a87d49a17d1a3a56f2fdf4d8252956f5d7e42bac21fd429622b083666',
        '79022071de3e7867b62d6bcc5c406873869b39c5',
    ),
    (
        'executive_brain/common/__init__.py',
        'legacy_quarantine/production/executive_brain/common/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/common/enums.py',
        'legacy_quarantine/production/executive_brain/common/enums.py.legacy',
        'a52965315e654ca657df47258e443e8b6aadbb1f38a83505c7a65c187ed7de0c',
        '7a7e8e4a862aff1218f0628b4e239ed818207f43',
    ),
    (
        'executive_brain/intent.py',
        'legacy_quarantine/production/executive_brain/intent.py.legacy',
        '5ec559d7657572d122b4e8314ce5cb4fa4af2aff14d2018e2f691294366844e6',
        '5f43d48d4d7ff5cadaef8454c86a2befbd1d73ff',
    ),
    (
        'executive_brain/managers/__init__.py',
        'legacy_quarantine/production/executive_brain/managers/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/managers/decision_manager.py',
        'legacy_quarantine/production/executive_brain/managers/decision_manager.py.legacy',
        'ca6b95e1a54aaf97283e5b8dcce90077e7551a51399d73679d3e4565781289b6',
        'e0f71b0f78afd0a443db5acdf265c2252bf9d163',
    ),
    (
        'executive_brain/managers/execution_manager.py',
        'legacy_quarantine/production/executive_brain/managers/execution_manager.py.legacy',
        '3afb70ab262a1c719da50bfe283b525812247f90a2d8f3265c59946be45229a7',
        '9aa525907ccefc7dd628df7f01cb148c101e7939',
    ),
    (
        'executive_brain/managers/mission_manager.py',
        'legacy_quarantine/production/executive_brain/managers/mission_manager.py.legacy',
        '163bdb92ca057333f21e024adc9bfb34adb521a9d45585805a56d520f88a2192',
        '764c12b60b26df084437f86a99905a8a907286ff',
    ),
    (
        'executive_brain/managers/planning_manager.py',
        'legacy_quarantine/production/executive_brain/managers/planning_manager.py.legacy',
        '2fdab0f81378825fc9b31a739cbb44bcca807456815b0af07a28b689c6a17ea5',
        '69e22b7d60db7cf91a4ff71ba59f1831e1613c68',
    ),
    (
        'executive_brain/managers/registry_manager.py',
        'legacy_quarantine/production/executive_brain/managers/registry_manager.py.legacy',
        'e9d3d8eee3dbf133fa346541d3690d316bd586ea6ca925e325fd0b960979c2d7',
        'c11d40f0621b43ace4579363fa7f6f7cde371198',
    ),
    (
        'executive_brain/managers/result_manager.py',
        'legacy_quarantine/production/executive_brain/managers/result_manager.py.legacy',
        'c6ff7e64b1d5e07d3d8a90504299066d9da3a0ac8a35c6029b9ca14f32ceab45',
        '505b66e1e948b176637601474877813e85f76a16',
    ),
    (
        'executive_brain/memory/__init__.py',
        'legacy_quarantine/production/executive_brain/memory/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/memory/memory_manager.py',
        'legacy_quarantine/production/executive_brain/memory/memory_manager.py.legacy',
        'e6c728007ae18e56ae8f7e9dd305e033d20326d80bd28c272d66131887ed4405',
        'e85118e26714e25db8028983ce5e5c682abffa47',
    ),
    (
        'executive_brain/memory/memory_registry.py',
        'legacy_quarantine/production/executive_brain/memory/memory_registry.py.legacy',
        'b3e12a5a0ec2e3a9a2b5f6c0fdd1d0aa0edfd9915c3f17cfed96c1cbdffe2d97',
        '34b671274a46da86657b0d5d6fe3a882e4a2f6d0',
    ),
    (
        'executive_brain/memory/working_memory.py',
        'legacy_quarantine/production/executive_brain/memory/working_memory.py.legacy',
        'ff7f567a9765202bda71fc92c6772a5c043f25394637e485dac9181a6bce1c11',
        'b38ba268dca51d4850951c28423added2c4b5bdf',
    ),
    (
        'executive_brain/models/__init__.py',
        'legacy_quarantine/production/executive_brain/models/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/models/context_snapshot_model.py',
        'legacy_quarantine/production/executive_brain/models/context_snapshot_model.py.legacy',
        '9e2278aa649f19abf985ba05850a6a1c131a4a5d30d3151d39bfecb50b077814',
        '24f744ee8c906213d92bfadafb3953a251855cc5',
    ),
    (
        'executive_brain/models/decision_model.py',
        'legacy_quarantine/production/executive_brain/models/decision_model.py.legacy',
        'deceeee997d672e73cf04e2930ee3a7839529bb5f05ece578f0f8b2238ec0f26',
        'c6b036f8505289eb50ca2b251a70067f4ea2cc52',
    ),
    (
        'executive_brain/models/execution_plan_model.py',
        'legacy_quarantine/production/executive_brain/models/execution_plan_model.py.legacy',
        'a080419965ecb23e8459fd1c8a117fca92d39d964d14726ffebd6d2eedec5cd6',
        '8599b02b89af0e9e7d237a4ad323690b6c497677',
    ),
    (
        'executive_brain/models/goal_model.py',
        'legacy_quarantine/production/executive_brain/models/goal_model.py.legacy',
        '8868b1096b83dfc5a0e4670a695134b9d0b440f235df70cf7857b105c1ba0684',
        'd6f87ace400f8ddfc17b73aec421d331d8bb1c3b',
    ),
    (
        'executive_brain/models/intent_model.py',
        'legacy_quarantine/production/executive_brain/models/intent_model.py.legacy',
        'e894f1cb3b1741e8edab581d159db384140bda66233ca33ac8fadf951b9204c4',
        '327bfd5fe9e82b00f142a12982ddf330cd2bb3b0',
    ),
    (
        'executive_brain/models/mission_model.py',
        'legacy_quarantine/production/executive_brain/models/mission_model.py.legacy',
        '552b761214a9b4cc875a2ea730ce17852bf0f191586e5e014b7790b81b07b45e',
        '3b722a1d6627bb576c40b59fbfea9a7d7b8666ef',
    ),
    (
        'executive_brain/models/result_model.py',
        'legacy_quarantine/production/executive_brain/models/result_model.py.legacy',
        '138a175e6d503b7c2e07c372cd407b03713386130af8fadbfa2fe1d1784de0c5',
        'ed99ab110ca751e279948b1a57cd88b52e5189c5',
    ),
    (
        'executive_brain/pipeline/executive_pipeline.py',
        'legacy_quarantine/production/executive_brain/pipeline/executive_pipeline.py.legacy',
        'bf8b105c0de804d67ecf95b53861d00295c9f257038ac6ad68667f7a1239da0b',
        'e80c3db6376df497c9f302938524e10c9647743c',
    ),
    (
        'executive_brain/planner/__init__.py',
        'legacy_quarantine/production/executive_brain/planner/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/registries/__init__.py',
        'legacy_quarantine/production/executive_brain/registries/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
    (
        'executive_brain/registries/base_registry.py',
        'legacy_quarantine/production/executive_brain/registries/base_registry.py.legacy',
        '0b5192ab84dae8b473949c09af498230193701fdd854d6a55509216258f11a08',
        '9f223a34c6585fa58e85311ba810933ee95e40d3',
    ),
    (
        'executive_brain/registries/decision_registry.py',
        'legacy_quarantine/production/executive_brain/registries/decision_registry.py.legacy',
        'e085fdb64cad672eca2559fd26a8596590b69fae60300e48cfbe718a6e2f5031',
        '83c16f1079a4f9d383267c82302f125eb8e09a6e',
    ),
    (
        'executive_brain/registries/execution_plan_registry.py',
        'legacy_quarantine/production/executive_brain/registries/execution_plan_registry.py.legacy',
        '00c4e82bf2bc4d0b4fb8b6d5def67c0d7b6d68634aa10dae35939dc010fb3c24',
        '32eaa1e981314a87fc96cea6d499445fd2510a38',
    ),
    (
        'executive_brain/registries/goal_registry.py',
        'legacy_quarantine/production/executive_brain/registries/goal_registry.py.legacy',
        'b874a1299dd0ccf08cf7cbf046b5dd798f8572e972bfc8e930dc515f943d3490',
        '1d4f2220c2c7434b8f6db4ddbc0183b55e04ca49',
    ),
    (
        'executive_brain/registries/intent_registry.py',
        'legacy_quarantine/production/executive_brain/registries/intent_registry.py.legacy',
        '08c9e3090fe437f7543594b00b2562ed34e9dcf0496848a4bb8b740b7908e481',
        'c3f44a29c016b364a361f6f1b786cc1cbe8b9c88',
    ),
    (
        'executive_brain/registries/mission_registry.py',
        'legacy_quarantine/production/executive_brain/registries/mission_registry.py.legacy',
        'b39d3383026de0010ed273441b8b91466304c9136872aa19ccacc410664157ef',
        'de0d1660573e0af1f2f0181bb8c801f0d34d69d9',
    ),
    (
        'executive_brain/registries/result_registry.py',
        'legacy_quarantine/production/executive_brain/registries/result_registry.py.legacy',
        '5dce7b02020cfbe7b4d474033d311b0f27260c8a32104125d7953006030891b0',
        '73af691da99a45bb49c4608e4dc20944989fc35b',
    ),
    (
        'executive_brain/timeline/__init__.py',
        'legacy_quarantine/production/executive_brain/timeline/__init__.py.legacy',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    ),
)
_F06E_EXECUTIVE_FINAL_SIZES_AND_CRLF = {
    'executive_brain/__init__.py': (0, 0),
    'executive_brain/brain/__init__.py': (0, 0),
    'executive_brain/brain/executive_brain.py': (6317, 168),
    'executive_brain/common/__init__.py': (0, 0),
    'executive_brain/common/enums.py': (322, 16),
    'executive_brain/intent.py': (1264, 65),
    'executive_brain/managers/__init__.py': (0, 0),
    'executive_brain/managers/decision_manager.py': (2762, 90),
    'executive_brain/managers/execution_manager.py': (2896, 93),
    'executive_brain/managers/mission_manager.py': (3248, 112),
    'executive_brain/managers/planning_manager.py': (2497, 85),
    'executive_brain/managers/registry_manager.py': (2311, 64),
    'executive_brain/managers/result_manager.py': (2476, 84),
    'executive_brain/memory/__init__.py': (0, 0),
    'executive_brain/memory/memory_manager.py': (2340, 84),
    'executive_brain/memory/memory_registry.py': (916, 27),
    'executive_brain/memory/working_memory.py': (2167, 58),
    'executive_brain/models/__init__.py': (0, 0),
    'executive_brain/models/context_snapshot_model.py': (1586, 61),
    'executive_brain/models/decision_model.py': (1680, 55),
    'executive_brain/models/execution_plan_model.py': (1432, 48),
    'executive_brain/models/goal_model.py': (1309, 38),
    'executive_brain/models/intent_model.py': (1386, 40),
    'executive_brain/models/mission_model.py': (2068, 59),
    'executive_brain/models/result_model.py': (1251, 45),
    'executive_brain/pipeline/executive_pipeline.py': (851, 26),
    'executive_brain/planner/__init__.py': (0, 0),
    'executive_brain/registries/__init__.py': (0, 0),
    'executive_brain/registries/base_registry.py': (1216, 46),
    'executive_brain/registries/decision_registry.py': (1039, 34),
    'executive_brain/registries/execution_plan_registry.py': (3145, 102),
    'executive_brain/registries/goal_registry.py': (1688, 56),
    'executive_brain/registries/intent_registry.py': (702, 24),
    'executive_brain/registries/mission_registry.py': (2733, 99),
    'executive_brain/registries/result_registry.py': (2355, 83),
    'executive_brain/timeline/__init__.py': (0, 0),
}
_F06E_EXECUTIVE_ALL_ARCHIVE_RECORDS = (
    *_F06E_EXECUTIVE_AI_ARCHIVE_RECORDS,
    *_F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS,
    *_F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS,
)
_F06E_EXECUTIVE_FINAL_EXCLUDED_IMPORTS = {
    'tests/base_registry_test.py': (
        ('executive_brain.registries.base_registry', 'executive_brain.registries.base_registry.BaseRegistry'),
    ),
    'tests/context_snapshot_model_test.py': (
        ('executive_brain.models.context_snapshot_model', 'executive_brain.models.context_snapshot_model.ContextSnapshotModel'),
    ),
    'tests/decision_model_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.decision_model', 'executive_brain.models.decision_model.DecisionModel'),
    ),
    'tests/decision_registry_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.decision_model', 'executive_brain.models.decision_model.DecisionModel'),
        ('executive_brain.registries.decision_registry', 'executive_brain.registries.decision_registry.DecisionRegistry'),
    ),
    'tests/execution_plan_model_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.execution_plan_model', 'executive_brain.models.execution_plan_model.ExecutionPlanModel'),
    ),
    'tests/goal_model_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.Priority'),
        ('executive_brain.models.goal_model', 'executive_brain.models.goal_model.GoalModel'),
    ),
    'tests/goal_registry_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus', 'executive_brain.common.enums.Priority'),
        ('executive_brain.models.goal_model', 'executive_brain.models.goal_model.GoalModel'),
        ('executive_brain.registries.goal_registry', 'executive_brain.registries.goal_registry.GoalRegistry'),
    ),
    'tests/intent_model_test.py': (
        ('executive_brain.models.intent_model', 'executive_brain.models.intent_model.IntentModel'),
    ),
    'tests/intent_registry_test.py': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus', 'executive_brain.common.enums.Priority'),
        ('executive_brain.models.intent_model', 'executive_brain.models.intent_model.IntentModel'),
        ('executive_brain.registries.intent_registry', 'executive_brain.registries.intent_registry.IntentRegistry'),
    ),
    'tests/intent_test.py': (
        ('executive_brain.intent', 'executive_brain.intent.Intent'),
    ),
    'tests/mission_model_test.py': (
        ('executive_brain.models.mission_model', 'executive_brain.models.mission_model.MissionModel'),
    ),
    'tests/result_model_test.py': (
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
    ),
}
_F06E_EXECUTIVE_FINAL_ARCHIVED_TEST_IMPORTS = {
    'legacy_quarantine/tests/executive/brain/test_executive_brain.py.legacy': (
        ('executive_brain.brain.executive_brain', 'executive_brain.brain.executive_brain.ExecutiveBrain'),
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
    ),
    'legacy_quarantine/tests/executive/managers/test_decision_manager.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.managers.decision_manager', 'executive_brain.managers.decision_manager.DecisionManager'),
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.models.decision_model', 'executive_brain.models.decision_model.DecisionModel'),
    ),
    'legacy_quarantine/tests/executive/managers/test_execution_manager.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.managers.execution_manager', 'executive_brain.managers.execution_manager.ExecutionManager'),
        ('executive_brain.managers.planning_manager', 'executive_brain.managers.planning_manager.PlanningManager'),
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
    ),
    'legacy_quarantine/tests/executive/managers/test_mission_manager.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.managers.mission_manager', 'executive_brain.managers.mission_manager.MissionManager'),
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.models.mission_model', 'executive_brain.models.mission_model.MissionModel'),
    ),
    'legacy_quarantine/tests/executive/managers/test_planning_manager.py.legacy': (
        ('executive_brain.managers.planning_manager', 'executive_brain.managers.planning_manager.PlanningManager'),
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.models.execution_plan_model', 'executive_brain.models.execution_plan_model.ExecutionPlanModel'),
    ),
    'legacy_quarantine/tests/executive/managers/test_registry_manager.py.legacy': (
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
        ('executive_brain.registries.decision_registry', 'executive_brain.registries.decision_registry.DecisionRegistry'),
        ('executive_brain.registries.execution_plan_registry', 'executive_brain.registries.execution_plan_registry.ExecutionPlanRegistry'),
        ('executive_brain.registries.goal_registry', 'executive_brain.registries.goal_registry.GoalRegistry'),
        ('executive_brain.registries.intent_registry', 'executive_brain.registries.intent_registry.IntentRegistry'),
        ('executive_brain.registries.mission_registry', 'executive_brain.registries.mission_registry.MissionRegistry'),
        ('executive_brain.registries.result_registry', 'executive_brain.registries.result_registry.ResultRegistry'),
    ),
    'legacy_quarantine/tests/executive/managers/test_result_manager.py.legacy': (
        ('executive_brain.managers.registry_manager', 'executive_brain.managers.registry_manager.RegistryManager'),
        ('executive_brain.managers.result_manager', 'executive_brain.managers.result_manager.ResultManager'),
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
    ),
    'legacy_quarantine/tests/executive/pipeline/test_executive_pipeline.py.legacy': (
        ('executive_brain.brain.executive_brain', 'executive_brain.brain.executive_brain.ExecutiveBrain'),
    ),
    'legacy_quarantine/tests/executive/pipeline/test_executive_pipeline_v2.py.legacy': (
        ('executive_brain.pipeline.executive_pipeline', 'executive_brain.pipeline.executive_pipeline.ExecutivePipeline'),
    ),
    'legacy_quarantine/tests/executive/registries/test_execution_plan_registry.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.execution_plan_model', 'executive_brain.models.execution_plan_model.ExecutionPlanModel'),
        ('executive_brain.registries.execution_plan_registry', 'executive_brain.registries.execution_plan_registry.ExecutionPlanRegistry'),
    ),
    'legacy_quarantine/tests/executive/registries/test_mission_registry.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.mission_model', 'executive_brain.models.mission_model.MissionModel'),
        ('executive_brain.registries.mission_registry', 'executive_brain.registries.mission_registry.MissionRegistry'),
    ),
    'legacy_quarantine/tests/executive/registries/test_result_registry.py.legacy': (
        ('executive_brain.common.enums', 'executive_brain.common.enums.LifecycleStatus'),
        ('executive_brain.models.result_model', 'executive_brain.models.result_model.ResultModel'),
        ('executive_brain.registries.result_registry', 'executive_brain.registries.result_registry.ResultRegistry'),
    ),
    'legacy_quarantine/tests/executive/runtime/test_executive_runtime.py.legacy': (
        ('executive_brain.brain.executive_brain', 'executive_brain.brain.executive_brain.ExecutiveBrain'),
    ),
    'legacy_quarantine/tests/integration/test_memory_runtime_integration.py.legacy': (
        ('executive_brain.brain.executive_brain', 'executive_brain.brain.executive_brain.ExecutiveBrain'),
        ('executive_brain.memory.memory_manager', 'executive_brain.memory.memory_manager.MemoryManager'),
    ),
    'legacy_quarantine/tests/memory/test_memory_manager.py.legacy': (
        ('executive_brain.memory.memory_manager', 'executive_brain.memory.memory_manager.MemoryManager'),
    ),
    'legacy_quarantine/tests/memory/test_memory_registry.py.legacy': (
        ('executive_brain.memory.memory_registry', 'executive_brain.memory.memory_registry.MemoryRegistry'),
        ('executive_brain.memory.working_memory', 'executive_brain.memory.working_memory.WorkingMemory'),
    ),
    'legacy_quarantine/tests/memory/test_working_memory.py.legacy': (
        ('executive_brain.memory.working_memory', 'executive_brain.memory.working_memory.WorkingMemory'),
    ),
}
_F06E_EXECUTIVE_FINAL_DEBT_SHA256 = {
    'legacy_quarantine/production/core/kernel.py.legacy':
        '12614a613c9156be0dee4aaab6630e161efd04f49b169ce97d27e321086fa86f',
    'legacy_quarantine/tests/executive/brain/test_executive_brain.py.legacy':
        'd422566f036ba637241e03f66f75aa80238aead422a30b54fd18d900126060cb',
    'legacy_quarantine/tests/executive/managers/test_decision_manager.py.legacy':
        'ba1b17667115e75129ed8b5c27a24a433b96d71991ddcd7ea6c763588cef4e5a',
    'legacy_quarantine/tests/executive/managers/test_execution_manager.py.legacy':
        '229639f71adbcb519c62fc1fee8c7f4b708169d469115f61fdd45971c1d88997',
    'legacy_quarantine/tests/executive/managers/test_mission_manager.py.legacy':
        '60b4d90e80ca2750109fcfae23e1c42b960302ee0fb6dd9eeccc9640af193b88',
    'legacy_quarantine/tests/executive/managers/test_planning_manager.py.legacy':
        'a56b590b241de2aec25b1bfa3c6c1f513ccd91e3d134cd963a5d0054adbea516',
    'legacy_quarantine/tests/executive/managers/test_registry_manager.py.legacy':
        '473bd4914180c0be406bb69a319183c5759149ec75b1cf8614e44390419eadcd',
    'legacy_quarantine/tests/executive/managers/test_result_manager.py.legacy':
        '15c84c43aadbecc91a0e8f82cd8e300510c9ad5c7909b5b973f06e16ec52e628',
    'legacy_quarantine/tests/executive/pipeline/test_executive_pipeline.py.legacy':
        '8be05bbee311ec57f528cb6fe3da2120a54e66f70a8ba5f7949ec59cc5aebe8c',
    'legacy_quarantine/tests/executive/pipeline/test_executive_pipeline_v2.py.legacy':
        '31430e092c95a4b48e0c1a05a03ecce6a30b58ce008a7adb8b04efc442016e23',
    'legacy_quarantine/tests/executive/registries/test_execution_plan_registry.py.legacy':
        '6174dd08b9ad419684b4994f0bc2ebe2053892cad804959bd8916efbb647a111',
    'legacy_quarantine/tests/executive/registries/test_mission_registry.py.legacy':
        'e91aadb273f1175d424ad4e4a5a70e4c39aebfc1256931bba4677a2803c6b0e6',
    'legacy_quarantine/tests/executive/registries/test_result_registry.py.legacy':
        'ae977136dcd578136ba074d9bd741d6c69f1fbd710e103aa382508be0440ea7e',
    'legacy_quarantine/tests/executive/runtime/test_executive_runtime.py.legacy':
        '945a3d4104883f62382a79f6a9c311f6102cfad67fa864c315e4e09c509558b7',
    'legacy_quarantine/tests/integration/test_memory_runtime_integration.py.legacy':
        '83bdf8e9cfd5b01fc9b487b4a1d9928fd30e14128beded4a226a97b7f30b9024',
    'legacy_quarantine/tests/memory/test_memory_manager.py.legacy':
        '1c888f4d7c9950a2f1090fe06d8dff3de77ea9d7bdbc02c49a73fa5b5e90b094',
    'legacy_quarantine/tests/memory/test_memory_registry.py.legacy':
        'b2503c77d160f01dd9c6a3b284086862cb27da297f52b78f5a39abdd0013378e',
    'legacy_quarantine/tests/memory/test_working_memory.py.legacy':
        'a09fa6bb85e7716d1622a2d75275963ba0081ac8ba36bee05bbcba76e35bb353',
    'tests/base_registry_test.py':
        '3a0571552b35bb44229aed523267f0a32adb248e332b2971ef7018f0ac0a1697',
    'tests/context_snapshot_model_test.py':
        'a90df95582d39ce86675310555b2a6ab033bc9329deed318d5eab7e652f3ae89',
    'tests/decision_model_test.py':
        '68a51a1e7182b20655fae4332067c81a7d55e4ede02848d25a1af27911708e4d',
    'tests/decision_registry_test.py':
        'c2a53e4b175ae3fe317bdd13742ebf60b9f817415e21d1cd0df122f24b1842e1',
    'tests/execution_plan_model_test.py':
        '49c3e9fded0b45d1573844f7c4f7b43651cc625f0b6db5e7c8c05e4bce779523',
    'tests/goal_model_test.py':
        '9969ef85b690a7d0e9424badbae6c16caed2197422b3edecd6232a163a9435bb',
    'tests/goal_registry_test.py':
        'a58ba23a5bd67e6d3efedbc3d5d00d890756b8cc905a33e28d962710ad4fd73c',
    'tests/intent_model_test.py':
        'd3496f0c09c8e15979ea695c27701dc52c1cd30449953a9fed71ee890a9a6553',
    'tests/intent_registry_test.py':
        'ae885a60ce51c8c1b1aa683fd115ed8b63bd2fa509ef6ca5d05ccf2082683948',
    'tests/intent_test.py':
        '67cceaac0448ecc31232878c2573687fb4f2d32e07d2bb518914ba7effc01e9a',
    'tests/mission_model_test.py':
        '512ef476e15ec5958abafdf483603e31c9aed7141a25da46a8cd3fd2286b412b',
    'tests/result_model_test.py':
        '3ffebcc21b341664850c9e61faebfae6d5ac0e0baa45604eaaa4427864b97c2e',
}


def _f06e_final_import_names(node: ast.AST, package: list[str]) -> tuple[str, ...]:
    """Resolve static and literal loader edges without importing their targets."""

    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        prefix = package[:len(package) - node.level + 1] if node.level else []
        module = ".".join(prefix + ([node.module] if node.module else []))
        return (module,) + tuple(
            ".".join(part for part in (module, alias.name) if part)
            for alias in node.names
        )
    if isinstance(node, ast.Call) and node.args:
        function = (
            node.func.id if isinstance(node.func, ast.Name)
            else node.func.attr if isinstance(node.func, ast.Attribute) else None
        )
        argument = node.args[0]
        if (
            function in {"import_module", "__import__", "add_import"}
            and isinstance(argument, ast.Constant) and isinstance(argument.value, str)
        ):
            return (argument.value,)
    return ()


def test_f06e_executive_final_root_archive_fidelity(pytestconfig: pytest.Config) -> None:
    """All 91 historical sources survive as exact inert archives; none stays live."""

    records = _F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS
    assert len(records) == 36
    assert {r[0] for r in records} == set(_F06E_EXECUTIVE_TOOLS_REMAINING_SOURCES)
    assert set(_F06E_EXECUTIVE_FINAL_SIZES_AND_CRLF) == {r[0] for r in records}
    _assert_f06e_production_archive_payloads(
        _F06E_EXECUTIVE_ALL_ARCHIVE_RECORDS, {"executive_brain": 91}, pytestconfig,
    )
    sizes = []
    for former, archive, _sha256, _blob in records:
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        size, crlf = _F06E_EXECUTIVE_FINAL_SIZES_AND_CRLF[former]
        assert len(payload) == size
        assert payload.count(b"\r\n") == payload.count(b"\n") == crlf
        assert payload.count(b"\r") == crlf
        sizes.append(size)
    assert sum(sizes) == 53957
    assert sizes.count(0) == 9
    live = _REPOSITORY_ROOT / "executive_brain"
    assert not live.exists()
    assert not tuple(live.rglob("*.py"))
    assert not tuple(live.rglob("*.pyc"))
    assert not tuple(live.rglob("__pycache__"))
    assert importlib.machinery.PathFinder.find_spec(
        "executive_brain", [str(_REPOSITORY_ROOT)]
    ) is None
    assert len(_F06E_EXECUTIVE_AI_ARCHIVE_RECORDS) == 13
    assert len(_F06E_EXECUTIVE_TOOLS_ARCHIVE_RECORDS) == 42
    historical = _assert_f06e_executive_historical_inventory()
    # Last pre-AI-retirement checkpoint retains the complete original Git tree.
    result = subprocess.run(
        ["git", "ls-tree", "-r", "0627453", "--", "executive_brain"],
        cwd=_REPOSITORY_ROOT, capture_output=True, text=True, check=True, timeout=30,
    )
    original = {}
    for line in result.stdout.splitlines():
        mode, kind, blob, former = line.split()
        assert (mode, kind) == ("100644", "blob")
        original[former] = blob
    assert len(original) == len(historical) == 91
    assert {former: _git_blob_id(payload, path=former)
            for former, payload in historical.items()} == original


def test_f06e_executive_final_caller_authority_containment() -> None:
    """Retirement removes shadow authority and leaves only exact inert caller debt."""

    from tests.tests.platform.test_canonical_import_boundary import (
        analyze_import_closure,
    )

    module_paths = {
        former.removesuffix(".py").replace("/", ".").removesuffix(".__init__"): former
        for former, _archive, _sha, _blob in _F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS
    }
    graph: dict[str, set[str]] = {path: set() for path in module_paths.values()}
    internal_edges = []
    registry_importers = set()
    workflow_edges = set()
    for former, archive, _sha, _blob in _F06E_EXECUTIVE_FINAL_ARCHIVE_RECORDS:
        tree = ast.parse((_REPOSITORY_ROOT / archive).read_text(encoding="utf-8-sig"))
        package = former.removesuffix(".py").replace("/", ".").split(".")[:-1]
        for node in ast.walk(tree):
            names = _f06e_final_import_names(node, package)
            resolved = [name for name in names if name in module_paths]
            if resolved:
                target = module_paths[max(resolved, key=len)]
                internal_edges.append((former, target))
                graph[former].add(target)
            if "executive_brain.managers.registry_manager" in names:
                registry_importers.add(former)
            if "workflow.workflow_engine" in names:
                workflow_edges.add(former)
            # Exact immutable payloads plus bounded external imports preserve the
            # static no-writer/no-provider/no-execution adjudication.
            assert all(name.partition(".")[0] in {
                "executive_brain", "jaos_platform", "workflow", "dataclasses",
                "datetime", "enum", "typing", "uuid",
            } for name in names)
            if isinstance(node, ast.Call):
                assert ast.unparse(node.func) not in {
                    "open", "eval", "exec", "__import__", "importlib.import_module",
                }
    assert len(graph) == 36
    assert len(internal_edges) == 55
    assert registry_importers == _F06E_CORE_KERNEL_REGISTRY_INTERNAL_IMPORTERS
    assert workflow_edges == {"executive_brain/pipeline/executive_pipeline.py"}
    # A DAG of 36 nodes has exactly 36 singleton SCCs and no self-cycle.
    def visit(node: str, active: set[str], completed: set[str]) -> None:
        assert node not in active, ("cycle", node)
        if node in completed:
            return
        active.add(node)
        for target in graph[node]:
            visit(target, active, completed)
        active.remove(node)
        completed.add(node)

    completed: set[str] = set()
    for node in graph:
        visit(node, set(), completed)
    assert len(completed) == 36

    observed = {}
    base_consumers = set()
    contract_consumers = set()
    production_workflow_callers = set()
    for path in _repository_live_python_paths():
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        package = relpath.removesuffix(".py").replace("/", ".").split(".")[:-1]
        statements = []
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
            names = _f06e_final_import_names(node, package)
            assert not any(n == "legacy_quarantine" or n.startswith("legacy_quarantine.")
                           for n in names)
            if any(n == "executive_brain" or n.startswith("executive_brain.") for n in names):
                statements.append(names)
            if not relpath.startswith("tests/"):
                if any(n.endswith(".BasePlatformService") for n in names):
                    base_consumers.add(relpath)
                if any(n.endswith(".PlatformContract") for n in names):
                    contract_consumers.add(relpath)
                if any(n == "workflow" or n.startswith("workflow.") for n in names):
                    production_workflow_callers.add(relpath)
            if (
                (relpath == "run_jaos.py" or relpath.startswith(("jaos/", "jaos_platform/")))
                and isinstance(node, ast.Constant) and isinstance(node.value, str)
            ):
                value = node.value
                if all(part.isidentifier() for part in value.split(".")):
                    assert value != "executive_brain"
                    assert not value.startswith("executive_brain.")
        if statements:
            observed[relpath] = tuple(statements)
    assert observed == _F06E_EXECUTIVE_FINAL_EXCLUDED_IMPORTS
    assert len(observed) == 12
    assert sum(map(len, observed.values())) == 21
    conftest = _load_tests_conftest()
    assert all(conftest.is_excluded_legacy_module(_REPOSITORY_ROOT / p) for p in observed)
    assert not any(p.startswith("tests/tests/") for p in observed)
    assert all(p.startswith("tests/") for p in observed)
    assert base_consumers == set()
    _assert_f06e_workflow_historical_inventory()
    assert contract_consumers == set()
    assert production_workflow_callers == set()
    assert not (_REPOSITORY_ROOT / "executive_brain/managers/registry_manager.py").exists()
    assert not (_REPOSITORY_ROOT / "executive_brain/pipeline/executive_pipeline.py").exists()

    archived = {}
    for path in (_REPOSITORY_ROOT / "legacy_quarantine").rglob("*.py.legacy"):
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        if relpath.startswith("legacy_quarantine/production/executive_brain/"):
            continue
        statements = tuple(
            names for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig")))
            if (names := _f06e_final_import_names(node, []))
            if any(name in module_paths for name in names)
        )
        if statements:
            archived[relpath] = statements
    core = "legacy_quarantine/production/core/kernel.py.legacy"
    assert archived.pop(core) == ((
        "executive_brain.managers.registry_manager",
        "executive_brain.managers.registry_manager.RegistryManager",
    ),)
    assert archived == _F06E_EXECUTIVE_FINAL_ARCHIVED_TEST_IMPORTS
    assert len(archived) == 17
    assert sum(map(len, archived.values())) == 47
    for relpath, sha in _F06E_EXECUTIVE_FINAL_DEBT_SHA256.items():
        assert hashlib.sha256((_REPOSITORY_ROOT / relpath).read_bytes()).hexdigest() == sha

    _assert_f06e_executive_family_caller_containment("executive_brain.ai")
    composition = _REPOSITORY_ROOT / "jaos/composition/platform_composition.py"
    imports = {
        name for node in ast.walk(ast.parse(composition.read_text(encoding="utf-8")))
        for name in _f06e_final_import_names(node, [])
    }
    assert {
        "jaos.executive.controller.ExecutiveController",
        "jaos.memory.storage.memory_store.MemoryStore",
        "jaos.intelligence.conversation.ConversationOrchestrator",
    } <= imports
    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert len(closure["analyzed_files"]) == 207
    assert len(closure["reached_modules"]) == 206
    assert not any(n == "executive_brain" or n.startswith("executive_brain.")
                   for n in closure["reached_modules"])
    _assert_config_containment_preserved()


# Workflow baseline captured at 0a04ae2; payloads are inspected, never executed.
_F06E_WORKFLOW_ARCHIVE_RECORDS = (('workflow/__init__.py',
  'legacy_quarantine/production/workflow/__init__.py.legacy',
  'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
  'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'),
 ('workflow/automation_rules_engine.py',
  'legacy_quarantine/production/workflow/automation_rules_engine.py.legacy',
  '50a6b99cf56a92f8aaedeed18413156714358ac06f87abf8e4c0c4261b0c4369',
  'b03024da5a009254a3fd842912dc9a67eeebfe76'),
 ('workflow/dependency_manager.py',
  'legacy_quarantine/production/workflow/dependency_manager.py.legacy',
  'f65961110fcb376ab20479892b6042a7726f0d0990bc034142b4d9acb43d65b5',
  '0e257fe976c380b202a465f4afdb0259d238d853'),
 ('workflow/retry_recovery_engine.py',
  'legacy_quarantine/production/workflow/retry_recovery_engine.py.legacy',
  '871c387aefda2b8e016c202eb3390bcd5cee8477f2fc92976ed76e8bd704a2de',
  'ad5cac211d5e23205b52eb825208779509e9d49a'),
 ('workflow/scheduler.py',
  'legacy_quarantine/production/workflow/scheduler.py.legacy',
  'd465c29cdb6c6dbea6c448a66fff33a0b3d6c9cabaf374819b732557d40d575c',
  '46c4279e9d1bd1599c6711f79e40cbcc619a5851'),
 ('workflow/task_manager.py',
  'legacy_quarantine/production/workflow/task_manager.py.legacy',
  '8221c2a258bb7114019a6882e0be4a527c2895f269eea1e5243443f563106f08',
  '4dc03367e039160cd78f9415acd4d88c354a4b61'),
 ('workflow/task_queue.py',
  'legacy_quarantine/production/workflow/task_queue.py.legacy',
  '913b4a80557b1a00a2e7d1746675962990bfd83ab9cee9fee74d835a60f6889d',
  '74bfa035e2f9d935493d9a85b63fbb9265a374c0'),
 ('workflow/workflow_engine.py',
  'legacy_quarantine/production/workflow/workflow_engine.py.legacy',
  'bc27c5c52027549d24f2c7407f82aeb1a8b87cccad8109314f16a0122d87226f',
  'cb1d36997a7a980a01841bc08e32ad076c5e64f8'),
 ('workflow/workflow_monitor.py',
  'legacy_quarantine/production/workflow/workflow_monitor.py.legacy',
  '2d54c51fb9376fbc5638f6a11649d7d0b192d9e174fed83e4a96bc8fd4b88ea9',
  'a6a22ff72607133e586aedbae57b30700d99050d'))

_F06E_WORKFLOW_SIZES_AND_CRLF = {'workflow/__init__.py': (0, 0),
 'workflow/automation_rules_engine.py': (875, 49),
 'workflow/dependency_manager.py': (1072, 58),
 'workflow/retry_recovery_engine.py': (878, 49),
 'workflow/scheduler.py': (877, 49),
 'workflow/task_manager.py': (1086, 58),
 'workflow/task_queue.py': (1129, 61),
 'workflow/workflow_engine.py': (1218, 42),
 'workflow/workflow_monitor.py': (834, 45)}

_F06E_WORKFLOW_EXCLUDED_IMPORTS = {
    "tests/automation_rules_engine_test.py": [
        "from workflow.automation_rules_engine import AutomationRulesEngine"
    ],
    "tests/dependency_manager_test.py": [
        "from workflow.dependency_manager import DependencyManager"
    ],
    "tests/retry_recovery_engine_test.py": [
        "from workflow.retry_recovery_engine import RetryRecoveryEngine"
    ],
    "tests/task_manager_test.py": [
        "from workflow.task_manager import TaskManager"
    ],
    "tests/task_queue_test.py": [
        "from workflow.task_queue import TaskQueue"
    ],
    "tests/workflow_engine_test.py": [
        "from workflow.workflow_engine import WorkflowEngine"
    ],
    "tests/workflow_monitor_test.py": [
        "from workflow.workflow_monitor import WorkflowMonitor"
    ],
    "tests/workflow_platform_integration_test.py": [
        "from workflow.automation_rules_engine import AutomationRulesEngine",
        "from workflow.dependency_manager import DependencyManager",
        "from workflow.retry_recovery_engine import RetryRecoveryEngine",
        "from workflow.scheduler import Scheduler",
        "from workflow.task_manager import TaskManager",
        "from workflow.task_queue import TaskQueue",
        "from workflow.workflow_engine import WorkflowEngine",
        "from workflow.workflow_monitor import WorkflowMonitor"
    ]
}

_F06E_WORKFLOW_ARCHIVED_IMPORTS = {
    "legacy_quarantine/production/executive_brain/pipeline/executive_pipeline.py.legacy": [
        "from workflow.workflow_engine import WorkflowEngine"
    ],
    "legacy_quarantine/tests/integration/test_workflow_runtime_integration.py.legacy": [
        "from workflow.workflow_engine import WorkflowEngine"
    ]
}

_F06E_WORKFLOW_DEBT_SHA256 = {'legacy_quarantine/production/executive_brain/pipeline/executive_pipeline.py.legacy': 'bf8b105c0de804d67ecf95b53861d00295c9f257038ac6ad68667f7a1239da0b',
 'legacy_quarantine/tests/integration/test_workflow_runtime_integration.py.legacy': '6bbfc848eeb30af9788bc2f3ad0897810dec8f4c6ced072227f3ac8e808bf83b',
 'tests/automation_rules_engine_test.py': 'b6a0edae463255edac938702007267f758c1d0353d5281f1ade236c9a08a9e74',
 'tests/dependency_manager_test.py': '85527b28f6c8856f9f5326ca10ff67859961f381e5a800d60dff33fc6b94cac6',
 'tests/retry_recovery_engine_test.py': '0eae5c686358c925b07916d2418f8bf2cf7bd5343ec14914c63a5c25215238c3',
 'tests/task_manager_test.py': 'bcb6e56aff115b61d2f677fa20c42665b556e0bebbec41b0834ef832c5271785',
 'tests/task_queue_test.py': '96800edabe8980e53e84142fcda5db7f28d61558fc264189c79a4280f4875c1c',
 'tests/workflow_engine_test.py': '8c5a2ee665d00959c4785a2bbd39efb0f70828454c62246d852f55cb2182e40e',
 'tests/workflow_monitor_test.py': '2e2e378385add86c211368c4cddccdcfc7c0a7551184eb9b9652713f2486daf2',
 'tests/workflow_platform_integration_test.py': '8c7140817265d86bfce059352157c60831032b7f82aa70899f9c859aeb4562b3'}

_F06E_WORKFLOW_PRESERVED_OWNER_SHA256 = {'brain/behavior_tracker.py': 'e33c91f4a7ba8b062d435a62dfca777de1190e6b385c5f9d94970f06aea26797',
 'brain/crash_recovery_system.py': '623a152bd292295c8507abc1b0340a66dcb3f5bc60b4b8977707ab2e3ebd78f3',
 'brain/decision_record.py': 'b49dfac4e09ec5970af466271649f32dff99b5ff32cb0799ce114079cab44d90',
 'brain/goal_tracker.py': 'eaa5c371be2c2281ae76444d54ac495f198119dfdd76b313f9dcfc969cbdc6da',
 'brain/provider_memory.py': '4131c61131cb157c2e04ac007f983760f24f5ff5e5ed27d52752f390a1b4c60d',
 'brain/provider_router.py': '7a033cacb06b6342b5ccbaa6db5bb35a2dabaf3141b7e8c903e863b9d85465e2',
 'brain/reasoning_trace_logger.py': 'eda2ef8551b60cb67b167fd7082e12d1b71bbe89102eae0f93a28fc667d6d7aa',
 'brain/user_profile.py': '4bfc34fd0418876b7442ade65fcc07cf32c2ad73be6bc5110b9c78c382c116e3',
 'core/action_history.py': '34ba99bfdf9520d12650cc56e0d522620abdec4555303d71e9f4b63e80a4bc30',
 'core/backup_manager.py': '0bde3faa0294ee6ea1df76332c776f01e6a82601a399925c51c7c320662ca013',
 'core/config_manager.py': '1bac73fa937da8534ef6e5a9dcbf26b521512dd835c22359063a1949b4789611',
 'core/snapshot_manager.py': '2b4dfc386821a081caf6bdb406315eab65edcd107a843e4b62eb2d19bdc40c09',
 'jaos/composition/platform_composition.py': '3a1111dd0ed8ac83a4f29ffb919d62b5c8285751ee8ddd910f3440096dfa0047',
 'jaos/executive/controller.py': '118d904bb6fad0de1b8bb4f9fdf5a8bd5e75c79af4d2b4fa5e3a29d4c791d8b1',
 'jaos/executive/execution_coordinator.py': '6ecbf45d3b1d696016da1d370c0d6e9aad05f51b397ce8a0bbaee2aa5afd92f0',
 'jaos/executive/planner.py': 'ad89f389c7a9a200ab299bb034be5d785a92ae430315fd0ca467caff0f84ecc0',
 'jaos/tools/tool_approval.py': '719f6768a0873500a8218dba26ba8a80bfc30a24bb81357fee0cc0ef7a769b70',
 'jaos/tools/tool_audit.py': 'e868a8981f53e63aaa55370c3e4104c8c7eb7142bb6c0287afbc1394da91479e',
 'jaos/tools/tool_execution.py': 'f64f8271890a083f84688a5a53cfb1862b8768ceaffbedd494548292e815cf87',
 'jaos/tools/tool_manager.py': 'b1d4cd9629bf8c148e9e80fcd0a55fd671006a3365f3641f561b27dc80708f1e',
 'jaos/tools/tool_permissions.py': 'd77245af4a60c5ca460dae847d89dabfc667bc180a4537a72370a3d53a0415da',
 'jaos_platform/base_platform_service.py': '29220485e2eb57e8c60dea4406f292c2786ddb90cc4ca6226a8949a7bc34ae5a',
 'jaos_platform/platform_contract.py': '800876c6de79bf4da90c1847b6c01d86816139af93ac8e5b860cedfdeac6e172',
 'jaos_platform/runtime_state_inventory.py': 'f5488702d59ac727328cc9d82f0a7a5f011aceb993474a4933686eb72ea1a979',
 'memory/long_term_memory.py': '1cfdab9536197f5aa25315b215639fb8ef0012ec1cede7e1884ce6b977c83f01',
 'memory/memory_cleanup.py': '6bc2c23798fa6c58a0cd1e27937bc23859444fad17fd6b985a3826280ce992d6',
 'memory/memory_export.py': '60563bfa421311225a12c020fbf6795f1741a9c021eed32bff92380875dfb16a',
 'run_jaos.py': 'ada071ed9bb530a9b62f10bd51d0703de3c5435aadffd999822eab2da1cc2cc3',
 'scripts/generate_dg1_docs.py': 'a990ecf5d2baf352911cff90ba7ef52c21f97b0fa638663e45f47a6338029d54'}

_F06E_WORKFLOW_HISTORICAL_CALLS = {'logger.info',
 'logger.warning',
 'print',
 'priority_order.get',
 'self.dependencies.get',
 'self.dependencies.items',
 'self.dependencies.setdefault',
 'self.dependencies.setdefault(task, []).append',
 'self.failures.append',
 'self.queue.append',
 'self.queue.pop',
 'self.queue.sort',
 'self.rules.append',
 'self.runtime.events.publish',
 'self.schedules.append',
 'self.tasks.items',
 'self.workflows.get',
 'self.workflows.items',
 'super',
 'super().__init__'}

def _assert_f06e_workflow_historical_inventory() -> dict[str, bytes]:
    """Reconstruct every earlier workflow inventory from the exact inert archives."""

    payloads = {}
    for former, archive, sha256, blob in _F06E_WORKFLOW_ARCHIVE_RECORDS:
        assert not (_REPOSITORY_ROOT / former).exists()
        payload = (_REPOSITORY_ROOT / archive).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == sha256
        assert _git_blob_id(payload, path=former) == blob
        payloads[former] = payload
    inventory = "".join(
        former + "\0" + hashlib.sha256(payload).hexdigest() + "\n"
        for former, payload in sorted(payloads.items())
    )
    for baselines in (
        _F06E_SATELLITE_RETAINED_ROOT_HASHES,
        _F06E_KERNEL_RETAINED_SOURCE_INVENTORIES,
        _F06E_EXECUTIVE_AI_RETAINED_INVENTORIES,
    ):
        count, digest = baselines["workflow"]
        assert len(payloads) == count == 9
        assert hashlib.sha256(inventory.encode("utf-8")).hexdigest() == digest
    return payloads


def test_f06e_workflow_archive_fidelity(pytestconfig: pytest.Config) -> None:
    """CASE A: preserve nine exact sources without an executable workflow namespace."""

    records = _F06E_WORKFLOW_ARCHIVE_RECORDS
    _assert_f06e_production_archive_payloads(records, {"workflow": 9}, pytestconfig)
    historical = _assert_f06e_workflow_historical_inventory()
    result = subprocess.run(
        ["git", "ls-tree", "-r", "0a04ae2", "--", "workflow"],
        cwd=_REPOSITORY_ROOT, capture_output=True, text=True, check=True, timeout=30,
    )
    original = {}
    for line in result.stdout.splitlines():
        mode, kind, blob, former = line.split()
        assert (mode, kind) == ("100644", "blob")
        original[former] = blob
    assert original == {former: blob for former, _archive, _sha, blob in records}
    assert set(original) == set(_F06E_WORKFLOW_SIZES_AND_CRLF)
    for former, archive, _sha256, _blob in records:
        payload = historical[former]
        size, crlf = _F06E_WORKFLOW_SIZES_AND_CRLF[former]
        assert len(payload) == size
        assert payload.count(b"\r\n") == payload.count(b"\n") == crlf
        assert payload.count(b"\r") == crlf
        # Compare filesystem-derived Git mode without staging or writing an index.
        mode_probe = subprocess.run(
            ["git", "diff", "--no-index", "--raw", "--", "/dev/null", archive],
            cwd=_REPOSITORY_ROOT, capture_output=True, text=True, check=False, timeout=30,
        )
        assert mode_probe.returncode == 1, mode_probe.stderr
        assert mode_probe.stdout.split()[1] == "100644"
    assert sum(map(len, historical.values())) == 7969
    assert sum(not payload for payload in historical.values()) == 1
    live = _REPOSITORY_ROOT / "workflow"
    assert not live.exists()
    assert not tuple(live.rglob("*.py"))
    assert not tuple(live.rglob("*.pyc"))
    assert not tuple(live.rglob("__pycache__"))
    assert importlib.machinery.PathFinder.find_spec(
        "workflow", [str(_REPOSITORY_ROOT)]
    ) is None
    conftest = _load_tests_conftest()
    for relpath, sha256 in _F06E_WORKFLOW_DEBT_SHA256.items():
        path = _REPOSITORY_ROOT / relpath
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha256
        if relpath.startswith("tests/"):
            assert conftest.is_excluded_legacy_module(path)
            assert not relpath.startswith("tests/tests/")
        else:
            assert path.name.endswith(".py.legacy")
            assert not any(fnmatch.fnmatchcase(path.name, p)
                           for p in pytestconfig.getini("python_files"))


def test_f06e_workflow_caller_authority_containment() -> None:
    """CASE B: static retirement preserves canonical owners and exact inert debt."""

    from tests.tests.platform.test_canonical_import_boundary import (
        _manifest_classified_paths,
        analyze_import_closure,
    )

    observed = {}
    base_consumers = set()
    contract_consumers = set()
    configured_legacy = set()
    for path in _repository_live_python_paths():
        relpath = path.relative_to(_REPOSITORY_ROOT).as_posix()
        package = relpath.removesuffix(".py").replace("/", ".").split(".")[:-1]
        statements = []
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
            names = _f06e_final_import_names(node, package)
            assert not any(n == "legacy_quarantine" or n.startswith("legacy_quarantine.")
                           for n in names)
            if any(n == "workflow" or n.startswith("workflow.") for n in names):
                statements.append(ast.unparse(node))
            if not relpath.startswith("tests/"):
                if any(n.endswith(".BasePlatformService") for n in names):
                    base_consumers.add(relpath)
                if any(n.endswith(".PlatformContract") for n in names):
                    contract_consumers.add(relpath)
            if (
                (relpath == "run_jaos.py" or relpath.startswith(("jaos/", "jaos_platform/")))
                and isinstance(node, ast.Constant) and isinstance(node.value, str)
            ):
                assert node.value != "workflow"
                assert not node.value.startswith("workflow.")
        if statements:
            observed[relpath] = statements
        assert "workflow" not in _literal_dynamic_import_roots(path)
        if relpath.startswith("tests/tests/") and (
            _imported_top_level_roots(path) & _F06D2E_LEGACY_FACING_IMPORT_ROOTS
        ):
            configured_legacy.add(relpath)
    assert observed == _F06E_WORKFLOW_EXCLUDED_IMPORTS
    assert len(observed) == 8
    assert sum(map(len, observed.values())) == 15
    conftest = _load_tests_conftest()
    assert all(conftest.is_excluded_legacy_module(_REPOSITORY_ROOT / p) for p in observed)
    assert all(p.startswith("tests/") and not p.startswith("tests/tests/") for p in observed)
    assert base_consumers == contract_consumers == set()
    assert configured_legacy == _F06D_CORE_KERNEL_REMAINING_LEGACY_FACING_PATHS
    assert len(configured_legacy) == 1

    archived = {}
    for path in (_REPOSITORY_ROOT / "legacy_quarantine").rglob("*.py.legacy"):
        statements = [
            ast.unparse(node)
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig")))
            if any(n == "workflow" or n.startswith("workflow.")
                   for n in _f06e_final_import_names(node, []))
        ]
        if statements:
            archived[path.relative_to(_REPOSITORY_ROOT).as_posix()] = statements
    assert archived == _F06E_WORKFLOW_ARCHIVED_IMPORTS
    assert len(archived) == 2
    assert all(len(statements) == 1 for statements in archived.values())
    assert not (_REPOSITORY_ROOT / "executive_brain/pipeline/executive_pipeline.py").exists()

    graph = {}
    historical_calls = set()
    for former, archive, _sha256, _blob in _F06E_WORKFLOW_ARCHIVE_RECORDS:
        graph[former] = set()
        for node in ast.walk(ast.parse((_REPOSITORY_ROOT / archive).read_text("utf-8"))):
            names = _f06e_final_import_names(node, ["workflow"])
            assert all(n.partition(".")[0] in {"logs", "jaos_platform"} for n in names)
            graph[former].update(n for n in names if n == "workflow" or n.startswith("workflow."))
            if isinstance(node, ast.Call):
                historical_calls.add(ast.unparse(node.func))
    assert len(graph) == 9
    assert sum(map(len, graph.values())) == 0
    # Nine nodes with zero edges give nine singleton SCCs, no cycles or self-cycles.
    assert all(not targets for targets in graph.values())
    assert historical_calls == _F06E_WORKFLOW_HISTORICAL_CALLS
    # Immutable owners include the canonical permission/approval/audit chain,
    # compatibility abstractions, writer inventory and every declared F06F writer.
    for relpath, sha256 in _F06E_WORKFLOW_PRESERVED_OWNER_SHA256.items():
        assert not relpath.startswith("workflow/")
        assert hashlib.sha256((_REPOSITORY_ROOT / relpath).read_bytes()).hexdigest() == sha256
    execution = ast.parse((_REPOSITORY_ROOT / "jaos/tools/tool_execution.py").read_text("utf-8"))
    execute = next(n for n in ast.walk(execution)
                   if isinstance(n, ast.FunctionDef) and n.name == "execute")
    calls = sorted((n.lineno, ast.unparse(n.func)) for n in ast.walk(execute)
                   if isinstance(n, ast.Call))
    names = [name for _line, name in calls]
    assert names.index("self._permissions.authorize") < names.index(
        "self._approval_manager.require_approval"
    ) < names.index("tool.execute")
    assert any(line > next(line for line, name in calls if name == "tool.execute")
               and name == "self._audit_logger.record" for line, name in calls)
    closure = analyze_import_closure(_REPOSITORY_ROOT, "run_jaos.py")
    assert closure["violations"] == []
    assert len(closure["analyzed_files"]) == 207
    assert len(closure["reached_modules"]) == 206
    assert not any(n == "workflow" or n.startswith("workflow.")
                   for n in closure["reached_modules"])
    manifest = (_REPOSITORY_ROOT / "docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md").read_text("utf-8")
    classified = _manifest_classified_paths(manifest)
    assert classified["D"] == {"brain/", "core/", "main.py", "memory/"}
    assert "legacy_quarantine/production/workflow/" in classified["E"]
    assert {code: len(paths) for code, paths in classified.items()} == {
        "A": 10, "B": 1, "D": 4, "E": 15, "F": 3,
    }
    assert sum(map(len, classified.values())) == 33
    _assert_config_containment_preserved()
