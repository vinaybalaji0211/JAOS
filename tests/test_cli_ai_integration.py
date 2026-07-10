from jaos.cli.command_dispatcher import CommandDispatcher


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


def test_help_includes_ai_commands(capsys):
    dispatcher = CommandDispatcher()

    should_continue = dispatcher.dispatch("help")
    output = capsys.readouterr().out

    assert should_continue is True
    assert "status ai" in output
    assert "ai <prompt>" in output