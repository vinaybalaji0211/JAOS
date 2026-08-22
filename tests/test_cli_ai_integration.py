from jaos.ai.diagnostics.models import DiagnosticStatus as AIDiagnosticStatus
from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.executive.diagnostics.models import (
    DiagnosticStatus as ExecutiveDiagnosticStatus,
)


def test_status_includes_ai_platform(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("status")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "AI Platform: Ready" in output
    assert "AI Providers: 1" in output
    assert "Default AI Provider: mock" in output


def test_status_ai_command(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("status ai")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "AI Platform" in output
    assert "Healthy: True" in output
    assert "Message: AI Platform is online." in output
    assert "Provider Count: 1" in output
    assert "Default Provider: mock" in output
    assert "- mock" in output


def test_ai_prompt_command(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("ai hello JAOS")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "mock: [USER]" in output
    assert "hello JAOS" in output


def test_empty_ai_prompt_is_rejected(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("ai ")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "AI prompt cannot be empty." in output


def test_status_reports_ai_platform_not_ready_when_unhealthy(capsys, monkeypatch):
    dispatcher = CommandDispatcher()
    monkeypatch.setattr(
        dispatcher.ai_manager,
        "get_diagnostic_status",
        lambda: AIDiagnosticStatus(
            component="AI Platform",
            healthy=False,
            message="down",
            details={},
        ),
    )

    dispatcher.dispatch("status")
    output = capsys.readouterr().out

    assert "AI Platform: Not Ready" in output
    assert "AI Platform: Ready" not in output


def test_status_reports_tool_platform_not_ready_with_no_tools(capsys, monkeypatch):
    dispatcher = CommandDispatcher()
    monkeypatch.setattr(dispatcher.tool_manager, "list_tools", lambda: ())

    dispatcher.dispatch("status")
    output = capsys.readouterr().out

    assert "Tool Platform: Not Ready" in output
    assert "Tool Platform: Ready" not in output


def test_status_reports_executive_degraded_when_unhealthy(capsys, monkeypatch):
    dispatcher = CommandDispatcher()
    monkeypatch.setattr(
        dispatcher.executive,
        "get_status",
        lambda: ExecutiveDiagnosticStatus(
            component="Executive Platform",
            healthy=False,
            message="down",
            details={},
        ),
    )

    dispatcher.dispatch("status")
    output = capsys.readouterr().out

    assert "Executive Controller: Degraded" in output
    assert "Executive Controller: Online" not in output


def test_help_includes_ai_commands(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("help")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "status ai" in output
    assert "ai <prompt>" in output