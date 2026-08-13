import pytest

from jaos.ai.provider import AIProviderLifecycleState
from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.cli.shell import JAOSShell


def _mock_lifecycle(dispatcher: CommandDispatcher) -> AIProviderLifecycleState:
    return (
        dispatcher.ai_manager.get_provider_manager()
        .get_state("mock")
        .lifecycle
    )


def test_dispatch_exit_returns_false_and_shuts_down_mock_provider(capsys) -> None:
    dispatcher = CommandDispatcher()

    assert _mock_lifecycle(dispatcher) == AIProviderLifecycleState.INITIALIZED

    result = dispatcher.dispatch("exit")

    assert result is False
    assert _mock_lifecycle(dispatcher) == AIProviderLifecycleState.SHUTDOWN
    assert "Shutting down JAOS..." in capsys.readouterr().out


def test_dispatcher_shutdown_is_idempotent() -> None:
    dispatcher = CommandDispatcher()

    assert _mock_lifecycle(dispatcher) == AIProviderLifecycleState.INITIALIZED

    dispatcher.shutdown()
    dispatcher.shutdown()

    assert _mock_lifecycle(dispatcher) == AIProviderLifecycleState.SHUTDOWN


def test_shell_eof_returns_normally_and_shuts_down_provider(
    monkeypatch,
    capsys,
) -> None:
    shell = JAOSShell()

    assert _mock_lifecycle(shell.dispatcher) == AIProviderLifecycleState.INITIALIZED

    def raise_eof(_prompt: str = "") -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)

    shell.run()

    output = capsys.readouterr().out

    assert "Shutting down JAOS..." in output
    assert _mock_lifecycle(shell.dispatcher) == AIProviderLifecycleState.SHUTDOWN


def test_shell_unexpected_dispatch_error_still_shuts_down_and_reraises(
    monkeypatch,
) -> None:
    shell = JAOSShell()

    assert _mock_lifecycle(shell.dispatcher) == AIProviderLifecycleState.INITIALIZED

    monkeypatch.setattr("builtins.input", lambda _prompt="": "help")

    def raise_runtime(_command: str) -> bool:
        raise RuntimeError("unexpected dispatch failure")

    monkeypatch.setattr(shell.dispatcher, "dispatch", raise_runtime)

    with pytest.raises(RuntimeError, match="unexpected dispatch failure"):
        shell.run()

    assert _mock_lifecycle(shell.dispatcher) == AIProviderLifecycleState.SHUTDOWN
