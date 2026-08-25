from unittest.mock import MagicMock

import pytest

from jaos.ai import AIManager, ProviderManager
from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.executive.controller import ExecutiveController
from jaos.executive.models import ExecutiveResponse
from jaos.tools.tool_manager import ToolManager

INCOMPLETE_USAGE_CASES = (
    ("read", "Usage: read <path>"),
    ("write", "Usage: write <path> <content>"),
    ("write notes.txt", "Usage: write <path> <content>"),
    ("copy", "Usage: copy <source> <destination>"),
    ("copy source.txt", "Usage: copy <source> <destination>"),
    ("move", "Usage: move <source> <destination>"),
    ("move source.txt", "Usage: move <source> <destination>"),
    ("rename", "Usage: rename <source> <new_name>"),
    ("rename source.txt", "Usage: rename <source> <new_name>"),
    ("delete", "Usage: delete <path> --confirm"),
    ("search", "Usage: search <root> <pattern>"),
    ("search .", "Usage: search <root> <pattern>"),
    ("backup", "Usage: backup <source> <destination>"),
    ("backup source.txt", "Usage: backup <source> <destination>"),
)

COMPLETE_COMMANDS = (
    "read notes.txt",
    "write notes.txt hello",
    "copy source.txt dest.txt",
    "move source.txt dest.txt",
    "rename source.txt renamed.txt",
    "search . *.txt",
    "backup source.txt backup.txt",
)


@pytest.fixture
def dispatcher() -> CommandDispatcher:
    tool_manager = MagicMock(spec=ToolManager)
    ai_manager = MagicMock(spec=AIManager)
    ai_manager.get_provider_manager.return_value = MagicMock(spec=ProviderManager)
    executive = MagicMock(spec=ExecutiveController)
    return CommandDispatcher(
        tool_manager,
        ai_manager=ai_manager,
        executive=executive,
    )


@pytest.mark.parametrize(("command", "usage"), INCOMPLETE_USAGE_CASES)
def test_incomplete_filesystem_command_returns_exact_usage(
    dispatcher: CommandDispatcher,
    command: str,
    usage: str,
    capsys,
) -> None:
    result = dispatcher.dispatch(command)
    output = capsys.readouterr().out

    assert result is True
    assert usage in output
    dispatcher.executive.process.assert_not_called()
    dispatcher.ai_manager.generate.assert_not_called()


@pytest.mark.parametrize("command", COMPLETE_COMMANDS)
def test_complete_filesystem_command_reaches_executive(
    dispatcher: CommandDispatcher,
    command: str,
    capsys,
) -> None:
    dispatcher.executive.process.return_value = ExecutiveResponse(
        success=True,
        message="Task completed successfully.",
    )

    result = dispatcher.dispatch(command)
    output = capsys.readouterr().out

    assert result is True
    assert "Task completed successfully." in output
    dispatcher.executive.process.assert_called_once_with(command)
    dispatcher.ai_manager.generate.assert_not_called()


def test_delete_with_path_preserves_approval_path(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    dispatcher.executive.process.return_value = ExecutiveResponse(
        success=False,
        message="Approval required. Add --confirm to approve this action.",
    )

    result = dispatcher.dispatch("delete notes.txt")
    output = capsys.readouterr().out

    assert result is True
    assert "Approval required. Add --confirm to approve this action." in output
    dispatcher.executive.process.assert_called_once_with("delete notes.txt")
    dispatcher.ai_manager.generate.assert_not_called()


def test_delete_with_path_and_confirm_reaches_executive(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    dispatcher.executive.process.return_value = ExecutiveResponse(
        success=True,
        message="Task completed successfully.",
    )

    result = dispatcher.dispatch("delete notes.txt --confirm")
    output = capsys.readouterr().out

    assert result is True
    assert "Task completed successfully." in output
    dispatcher.executive.process.assert_called_once_with(
        "delete notes.txt --confirm"
    )
    dispatcher.ai_manager.generate.assert_not_called()


def test_unknown_command_reaches_existing_ai_fallback(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    dispatcher.executive.process.return_value = ExecutiveResponse(
        success=True,
        message="mock: [USER]\nunknown-command",
        output={"provider": "mock", "model": "mock-model"},
    )

    result = dispatcher.dispatch("unknown-command")
    output = capsys.readouterr().out

    assert result is True
    assert "unknown-command" in output
    assert "Provider: mock" in output
    dispatcher.executive.process.assert_called_once_with("unknown-command")
    dispatcher.ai_manager.generate.assert_not_called()


def test_free_form_text_reaches_existing_ai_fallback(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    dispatcher.executive.process.return_value = ExecutiveResponse(
        success=True,
        message="mock: [USER]\nExplain JAOS routing",
        output={"provider": "mock", "model": "mock-model"},
    )

    result = dispatcher.dispatch("Explain JAOS routing")
    output = capsys.readouterr().out

    assert result is True
    assert "Explain JAOS routing" in output
    assert "Provider: mock" in output
    dispatcher.executive.process.assert_called_once_with("Explain JAOS routing")
    dispatcher.ai_manager.generate.assert_not_called()


def test_empty_ai_prompt_retains_existing_validation(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    result = dispatcher.dispatch("ai")
    output = capsys.readouterr().out

    assert result is True
    assert "AI prompt cannot be empty." in output
    dispatcher.executive.process.assert_not_called()
    dispatcher.ai_manager.generate.assert_not_called()


def test_ai_prompt_retains_direct_ai_manager_behavior(
    dispatcher: CommandDispatcher,
    capsys,
) -> None:
    response = MagicMock()
    response.text = "mock: hello JAOS"
    dispatcher.ai_manager.generate.return_value = response

    result = dispatcher.dispatch("ai hello JAOS")
    output = capsys.readouterr().out

    assert result is True
    assert "mock: hello JAOS" in output
    dispatcher.ai_manager.generate.assert_called_once_with("hello JAOS")
    dispatcher.executive.process.assert_not_called()
