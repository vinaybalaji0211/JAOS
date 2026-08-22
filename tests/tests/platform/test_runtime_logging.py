from __future__ import annotations

import importlib
import inspect
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths
from logs.logger import (
    SYSTEM_LOG_FILENAME,
    configure_runtime_logging,
    logger,
    reset_runtime_logging,
)


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_RUNTIME_ENVIRONMENT_VARIABLES = (
    "JAOS_RUNTIME_DIR",
    "LOCALAPPDATA",
    "XDG_DATA_HOME",
    "HOME",
)


@pytest.fixture(autouse=True)
def clean_runtime_logging() -> None:
    reset_runtime_logging()
    yield
    reset_runtime_logging()


def _flush_jaos_handlers() -> None:
    for handler in logger.handlers:
        if getattr(handler, "_jaos_runtime_owned", False):
            handler.flush()


def _owned_handlers() -> list[logging.Handler]:
    return [
        handler
        for handler in logger.handlers
        if getattr(handler, "_jaos_runtime_owned", False)
    ]


def test_importing_logger_has_no_filesystem_side_effect(
    protected_repository_state,
    tmp_path: Path,
) -> None:
    environment = os.environ.copy()
    existing_python_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        path
        for path in (str(_REPOSITORY_ROOT), existing_python_path)
        if path
    )
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, "-c", "import logs.logger"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert tuple(tmp_path.iterdir()) == ()


def test_configuration_uses_only_injected_logs_scope(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    log_file = configure_runtime_logging(jaos_runtime_paths)

    assert log_file == jaos_runtime_paths.logs / SYSTEM_LOG_FILENAME
    assert jaos_runtime_paths.logs.is_dir()
    assert not log_file.exists()
    assert not jaos_runtime_paths.config.exists()
    assert not jaos_runtime_paths.memory.exists()
    assert not jaos_runtime_paths.state.exists()


def test_system_log_is_created_only_after_log_emission(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    log_file = configure_runtime_logging(jaos_runtime_paths)

    assert not log_file.exists()

    logger.info("fortress-02d-explicit-emission")
    _flush_jaos_handlers()

    assert log_file.is_file()
    assert "fortress-02d-explicit-emission" in log_file.read_text(
        encoding="utf-8"
    )


def test_logger_has_no_repository_path_or_private_resolver() -> None:
    logger_module = importlib.import_module("logs.logger")
    source = inspect.getsource(logger_module)
    repository_specific_path = "C:" + "\\JARVIS"

    assert repository_specific_path not in source
    assert "logs/system.log" not in source
    assert "Path.cwd(" not in source
    assert "os.getcwd(" not in source
    assert "RuntimePathResolver" not in source
    assert "basicConfig" not in source


def test_different_runtime_roots_are_isolated(
    tmp_path: Path,
    jaos_runtime_paths_factory,
) -> None:
    first_paths = jaos_runtime_paths_factory(tmp_path / "first")
    second_paths = jaos_runtime_paths_factory(tmp_path / "second")

    first_log = configure_runtime_logging(first_paths)
    logger.info("first-runtime-only")
    second_log = configure_runtime_logging(second_paths)
    logger.info("second-runtime-only")
    reset_runtime_logging()

    first_content = first_log.read_text(encoding="utf-8")
    second_content = second_log.read_text(encoding="utf-8")
    assert "first-runtime-only" in first_content
    assert "second-runtime-only" not in first_content
    assert "second-runtime-only" in second_content
    assert "first-runtime-only" not in second_content


def test_repeated_configuration_reuses_one_owned_handler(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    first_log = configure_runtime_logging(jaos_runtime_paths)
    second_log = configure_runtime_logging(jaos_runtime_paths)

    assert second_log == first_log
    assert len(_owned_handlers()) == 1


def test_reconfiguration_does_not_duplicate_log_entries(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    log_file = configure_runtime_logging(jaos_runtime_paths)
    configure_runtime_logging(jaos_runtime_paths)

    logger.info("single-fortress-entry")
    reset_runtime_logging()

    content = log_file.read_text(encoding="utf-8")
    assert content.count("single-fortress-entry") == 1


def test_reset_releases_windows_file_handle(
    tmp_path: Path,
    jaos_runtime_paths: RuntimePaths,
) -> None:
    log_file = configure_runtime_logging(jaos_runtime_paths)
    logger.info("release-the-file-handle")
    _flush_jaos_handlers()

    reset_runtime_logging()

    assert log_file.is_file()
    assert _owned_handlers() == []
    jaos_runtime_paths.runtime_root.relative_to(tmp_path)
    shutil.rmtree(jaos_runtime_paths.runtime_root)
    assert not jaos_runtime_paths.runtime_root.exists()


def test_reset_preserves_unrelated_handlers(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    unrelated_handler = logging.NullHandler()
    logger.addHandler(unrelated_handler)
    try:
        configure_runtime_logging(jaos_runtime_paths)

        reset_runtime_logging()

        assert unrelated_handler in logger.handlers
        assert _owned_handlers() == []
    finally:
        logger.removeHandler(unrelated_handler)
        unrelated_handler.close()


def test_logging_configuration_does_not_mutate_environment(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    before = {
        name: os.environ.get(name)
        for name in _RUNTIME_ENVIRONMENT_VARIABLES
    }

    configure_runtime_logging(jaos_runtime_paths)
    logger.info("environment-remains-unchanged")
    reset_runtime_logging()

    after = {
        name: os.environ.get(name)
        for name in _RUNTIME_ENVIRONMENT_VARIABLES
    }
    assert after == before


def test_platform_runtime_configures_its_owned_logs_scope(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    runtime = PlatformRuntime(runtime_paths=jaos_runtime_paths)

    assert not jaos_runtime_paths.runtime_root.exists()

    log_file = runtime.configure_logging()
    logger.info("platform-owned-runtime-logging")
    reset_runtime_logging()

    assert log_file == jaos_runtime_paths.logs / SYSTEM_LOG_FILENAME
    assert "platform-owned-runtime-logging" in log_file.read_text(
        encoding="utf-8"
    )


def test_runtime_logging_preserves_real_repository_trees(
    protected_repository_state,
    jaos_runtime_paths: RuntimePaths,
) -> None:
    log_file = configure_runtime_logging(jaos_runtime_paths)
    logger.info("temporary-runtime-only")
    reset_runtime_logging()

    assert log_file.is_file()
    with pytest.raises(ValueError):
        log_file.relative_to(_REPOSITORY_ROOT)
