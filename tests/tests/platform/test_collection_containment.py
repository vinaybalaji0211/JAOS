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
_F06D2C_DEFERRED_MEMORY_RUNTIME_PATH = (
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


def test_f06d2c_retires_only_the_authorized_executive_importers() -> None:
    """The adjacent legacy Memory/runtime test remains executable and deferred."""

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
    assert _F06D2C_DEFERRED_MEMORY_RUNTIME_PATH.is_file()
    assert (
        "tests/tests/integration/test_memory_runtime_integration.py"
        in executive_importers
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

_F06D2D_DEFERRED_MEMORY_IMPORTERS = frozenset(
    {
        "tests/tests/integration/test_memory_runtime_integration.py",
        "tests/tests/memory/test_memory_manager.py",
        "tests/tests/memory/test_memory_registry.py",
        "tests/tests/memory/test_working_memory.py",
    }
)

_F06D2D_DEFERRED_PROVIDER_IMPORTERS = frozenset(
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


def test_f06d2d_deferred_memory_and_provider_inventories_remain() -> None:
    """D2D's deferred Memory/provider residue remains after D2E retirement."""

    configured_root = _REPOSITORY_ROOT / "tests" / "tests"
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
    assert executive_importers == (
        _F06D2D_DEFERRED_MEMORY_IMPORTERS
        | _F06D2D_DEFERRED_PROVIDER_IMPORTERS
    )
    assert len(executive_importers) == 6
    assert len(retired_tool_importers) == 16
    assert len(_F06D2D_DEFERRED_MEMORY_IMPORTERS) == 4
    assert len(_F06D2D_DEFERRED_PROVIDER_IMPORTERS) == 2


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

_F06D2E_REMAINING_LEGACY_FACING_PATHS = frozenset(
    {
        "tests/tests/ai/test_ollama_provider.py",
        "tests/tests/ai/test_openai_provider.py",
        "tests/tests/integration/test_communication_runtime_integration.py",
        "tests/tests/integration/test_dashboard_runtime_integration.py",
        "tests/tests/integration/test_development_runtime_integration.py",
        "tests/tests/integration/test_engineering_runtime_integration.py",
        "tests/tests/integration/test_infrastructure_runtime_integration.py",
        "tests/tests/integration/test_knowledge_runtime_integration.py",
        "tests/tests/integration/test_memory_runtime_integration.py",
        "tests/tests/integration/test_pc_control_runtime_integration.py",
        "tests/tests/integration/test_security_runtime_integration.py",
        "tests/tests/integration/test_system_services_runtime_integration.py",
        "tests/tests/integration/test_workflow_runtime_integration.py",
        "tests/tests/memory/test_memory_manager.py",
        "tests/tests/memory/test_memory_registry.py",
        "tests/tests/memory/test_working_memory.py",
        "tests/tests/platform/test_config_containment.py",
        "tests/tests/platform/test_core_runtime_integration.py",
        "tests/tests/platform/test_kernel_runtime_integration.py",
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
    """D2E leaves exactly four Memory and two provider importers."""

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
    assert executive_importers == (
        _F06D2D_DEFERRED_MEMORY_IMPORTERS
        | _F06D2D_DEFERRED_PROVIDER_IMPORTERS
    )
    assert len(executive_importers) == 6
    assert legacy_facing_paths == _F06D2E_REMAINING_LEGACY_FACING_PATHS
    assert len(legacy_facing_paths) == 19

    assert len(_F06D2E_PRODUCTION_PROTOTYPE_PATHS) == 16
    for prototype_relpath in _F06D2E_PRODUCTION_PROTOTYPE_PATHS:
        assert (_REPOSITORY_ROOT / prototype_relpath).is_file()
