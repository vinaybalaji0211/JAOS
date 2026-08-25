from unittest.mock import MagicMock

import pytest

import jaos.cli.command_dispatcher as dispatcher_module
from jaos.ai import AIManager, ProviderManager
from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.cli.shell import JAOSShell
from jaos.executive.controller import ExecutiveController
from jaos.tools.tool_manager import ToolManager


@pytest.fixture
def collaborators() -> tuple[MagicMock, MagicMock, MagicMock]:
    tool_manager = MagicMock(spec=ToolManager)
    ai_manager = MagicMock(spec=AIManager)
    ai_manager.get_provider_manager.return_value = MagicMock(spec=ProviderManager)
    executive = MagicMock(spec=ExecutiveController)
    return tool_manager, ai_manager, executive


@pytest.fixture
def dispatcher(
    collaborators: tuple[MagicMock, MagicMock, MagicMock],
) -> CommandDispatcher:
    tool_manager, ai_manager, executive = collaborators
    return CommandDispatcher(
        tool_manager,
        ai_manager=ai_manager,
        executive=executive,
    )


def test_dispatch_exit_returns_false_without_owning_platform_shutdown(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    result = dispatcher.dispatch("exit")

    assert result is False
    assert "Shutting down JAOS..." in capsys.readouterr().out
    dispatcher.ai_manager.shutdown.assert_not_called()


def test_provider_helpers_are_read_only_views_of_injected_provider_state(
    collaborators: tuple[MagicMock, MagicMock, MagicMock],
) -> None:
    tool_manager, ai_manager, executive = collaborators
    provider_manager = ai_manager.get_provider_manager.return_value
    config = MagicMock()
    config.name = "mock"
    config.enabled = True
    config.secret_refs = ()
    config.requires_secrets.return_value = False
    state = MagicMock()
    state.enabled = True
    state.current_model = "mock-model"
    provider_manager.get_config.return_value = config
    provider_manager.get_state.return_value = state
    provider_manager.get_default_provider_name.return_value = "mock"

    dispatcher = CommandDispatcher(
        tool_manager,
        ai_manager=ai_manager,
        executive=executive,
    )
    status = dispatcher.provider_status.get_provider_status("mock")

    assert dispatcher.provider_status.provider_manager is provider_manager
    assert dispatcher.provider_profiles.has("mock") is True
    assert status.name == "mock"
    assert status.is_default is True
    provider_manager.get_config.assert_called_once_with("mock")
    provider_manager.get_state.assert_called_once_with("mock")
    provider_manager.get_default_provider_name.assert_called_once_with()
    for mutation in (
        "register_provider",
        "unregister_provider",
        "initialize_provider",
        "initialize_all",
        "shutdown_provider",
        "shutdown_all",
        "set_default_provider",
        "generate",
    ):
        getattr(provider_manager, mutation).assert_not_called()
    ai_manager.shutdown.assert_not_called()


def test_command_dispatcher_requires_all_collaborators(
    collaborators: tuple[MagicMock, MagicMock, MagicMock],
) -> None:
    tool_manager, ai_manager, executive = collaborators

    with pytest.raises(TypeError, match="tool_manager"):
        CommandDispatcher(  # type: ignore[call-arg]
            ai_manager=ai_manager,
            executive=executive,
        )

    with pytest.raises(TypeError, match="ai_manager"):
        CommandDispatcher(  # type: ignore[call-arg]
            tool_manager,
            executive=executive,
        )

    with pytest.raises(TypeError, match="executive"):
        CommandDispatcher(  # type: ignore[call-arg]
            tool_manager,
            ai_manager=ai_manager,
        )


@pytest.mark.parametrize(
    ("missing_name", "message"),
    (
        ("tool_manager", "tool_manager must not be None"),
        ("ai_manager", "ai_manager must not be None"),
        ("executive", "executive must not be None"),
    ),
)
def test_command_dispatcher_rejects_none_collaborators(
    collaborators: tuple[MagicMock, MagicMock, MagicMock],
    missing_name: str,
    message: str,
    monkeypatch,
) -> None:
    tool_manager, ai_manager, executive = collaborators
    build_profiles = MagicMock(
        side_effect=AssertionError("profile construction must not be reached")
    )
    build_provider_status = MagicMock(
        side_effect=AssertionError("status construction must not be reached")
    )
    monkeypatch.setattr(
        dispatcher_module.ProviderProfileRegistry,
        "build_default",
        build_profiles,
    )
    monkeypatch.setattr(
        dispatcher_module,
        "ProviderStatusService",
        build_provider_status,
    )
    dependencies = {
        "tool_manager": tool_manager,
        "ai_manager": ai_manager,
        "executive": executive,
    }
    dependencies[missing_name] = None

    with pytest.raises(TypeError, match=message):
        CommandDispatcher(**dependencies)  # type: ignore[arg-type]

    build_profiles.assert_not_called()
    build_provider_status.assert_not_called()
    ai_manager.get_provider_manager.assert_not_called()


def test_shell_requires_an_injected_dispatcher() -> None:
    with pytest.raises(TypeError):
        JAOSShell()  # type: ignore[call-arg]

    with pytest.raises(TypeError, match="dispatcher must not be None"):
        JAOSShell(None)  # type: ignore[arg-type]


def test_shell_eof_returns_normally_without_lifecycle_ownership(
    monkeypatch,
    capsys,
) -> None:
    dispatcher = MagicMock(spec=CommandDispatcher)
    shell = JAOSShell(dispatcher)

    def raise_eof(_prompt: str = "") -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)

    shell.run()

    assert "Shutting down JAOS..." in capsys.readouterr().out
    dispatcher.dispatch.assert_not_called()


def test_shell_unexpected_dispatch_error_reraises_without_lifecycle_ownership(
    monkeypatch,
) -> None:
    dispatcher = MagicMock(spec=CommandDispatcher)
    dispatcher.dispatch.side_effect = RuntimeError("unexpected dispatch failure")
    shell = JAOSShell(dispatcher)
    monkeypatch.setattr("builtins.input", lambda _prompt="": "help")

    with pytest.raises(RuntimeError, match="unexpected dispatch failure"):
        shell.run()

    dispatcher.dispatch.assert_called_once_with("help")
