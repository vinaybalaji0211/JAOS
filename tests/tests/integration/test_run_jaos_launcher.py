"""FORTRESS-04: run_jaos.py reaches the real PlatformRuntime lifecycle.

Every test injects the disposable ``jaos_runtime_paths`` fixture so
``JAOSApplication``'s ``configure_logging()`` call never resolves to (and
``mkdir``s under) the real OS-default runtime directory, per the FORTRESS-02
test-isolation contract.
"""

from __future__ import annotations

import builtins

import pytest

import run_jaos
from jaos.ai import AIManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths
from logs.logger import reset_runtime_logging
from run_jaos import JAOSApplication


@pytest.fixture(autouse=True)
def _reset_logging():
    """Every test exercises JAOSApplication.run(), which configures the
    shared JARVIS_OS logger singleton; reset it so no handler leaks across
    tests, matching test_runtime_logging.py's established pattern."""

    reset_runtime_logging()
    yield
    reset_runtime_logging()


def _raise_eof(_prompt: str = "") -> str:
    raise EOFError


def _track_ai_shutdown(monkeypatch) -> list[AIManager]:
    shutdown_calls: list[AIManager] = []
    original_shutdown = AIManager.shutdown

    def tracked_shutdown(ai_manager: AIManager) -> None:
        shutdown_calls.append(ai_manager)
        original_shutdown(ai_manager)

    monkeypatch.setattr(AIManager, "shutdown", tracked_shutdown)
    return shutdown_calls


def test_run_reaches_ready_then_stopped_on_clean_exit(
    monkeypatch, capsys, jaos_runtime_paths: RuntimePaths
):
    shutdown_calls = _track_ai_shutdown(monkeypatch)
    monkeypatch.setattr(builtins, "input", _raise_eof)

    app = JAOSApplication(runtime=PlatformRuntime(runtime_paths=jaos_runtime_paths))
    exit_code = app.run()

    capsys.readouterr()

    assert exit_code == 0
    assert len(shutdown_calls) == 1
    assert shutdown_calls[0]._shutdown_complete is True
    assert app.runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert app.runtime.container.list_services() == []


def test_run_explicit_exit_shuts_down_composed_ai_exactly_once(
    monkeypatch, capsys, jaos_runtime_paths: RuntimePaths
):
    shutdown_calls = _track_ai_shutdown(monkeypatch)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "exit")

    app = JAOSApplication(runtime=PlatformRuntime(runtime_paths=jaos_runtime_paths))
    exit_code = app.run()

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Shutting down JAOS..." in output
    assert len(shutdown_calls) == 1
    assert shutdown_calls[0]._shutdown_complete is True
    assert app.runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert app.runtime.container.list_services() == []


def test_run_configures_logging_through_runtime_paths(
    monkeypatch, capsys, jaos_runtime_paths: RuntimePaths
):
    monkeypatch.setattr(builtins, "input", _raise_eof)

    app = JAOSApplication(runtime=PlatformRuntime(runtime_paths=jaos_runtime_paths))
    app.run()

    capsys.readouterr()

    from logs.logger import logger

    owned_handlers = [
        handler
        for handler in logger.handlers
        if getattr(handler, "_jaos_runtime_owned", False)
    ]
    assert owned_handlers
    expected_path = jaos_runtime_paths.logs / "system.log"
    assert any(
        getattr(handler, "baseFilename", None) == str(expected_path)
        for handler in owned_handlers
    )


def test_run_returns_truthful_nonzero_on_boot_failure(
    monkeypatch, jaos_runtime_paths: RuntimePaths
):
    def _fail_if_called(_prompt: str = "") -> str:
        raise AssertionError("shell must not be reached when boot fails")

    monkeypatch.setattr(builtins, "input", _fail_if_called)

    runtime = PlatformRuntime(runtime_paths=jaos_runtime_paths)
    runtime.container.register("event_bus", object())

    app = JAOSApplication(runtime=runtime)
    exit_code = app.run()

    assert exit_code == 1
    assert app.runtime.lifecycle_state == RuntimeLifecycleState.FAILED


def test_run_controls_shutdown_on_shell_exception(
    monkeypatch, jaos_runtime_paths: RuntimePaths
):
    shutdown_calls = _track_ai_shutdown(monkeypatch)

    class BrokenShell:
        def __init__(self, dispatcher) -> None:
            self.dispatcher = dispatcher

        def run(self) -> None:
            raise RuntimeError("shell execution exploded")

    monkeypatch.setattr(run_jaos, "JAOSShell", BrokenShell)

    app = JAOSApplication(runtime=PlatformRuntime(runtime_paths=jaos_runtime_paths))
    exit_code = app.run()

    assert exit_code == 1
    assert len(shutdown_calls) == 1
    assert shutdown_calls[0]._shutdown_complete is True
    assert app.runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert app.runtime.container.list_services() == []


def test_run_makes_no_unconditional_status_claim_on_success(
    monkeypatch, capsys, jaos_runtime_paths: RuntimePaths
):
    monkeypatch.setattr(builtins, "input", _raise_eof)

    app = JAOSApplication(runtime=PlatformRuntime(runtime_paths=jaos_runtime_paths))
    app.run()

    output = capsys.readouterr().out

    assert "Boot Complete" not in output
    assert "Ready" not in output
