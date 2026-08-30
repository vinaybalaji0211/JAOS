import os

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.close_application_tool import (
    CloseApplicationTool,
)


def test_close_application_tool_name():
    tool = CloseApplicationTool()

    assert tool.tool_name == "close_application"


def test_close_application_success(monkeypatch):
    called = {}

    def fake_kill(pid, signal):
        called["pid"] = pid
        called["signal"] = signal

    monkeypatch.setattr(os, "kill", fake_kill)

    tool = CloseApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="close_application",
            parameters={"pid": 1234},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Application closed successfully"
    assert response.data["pid"] == 1234

    assert called["pid"] == 1234
    assert called["signal"] == 9


def test_close_application_failure(monkeypatch):
    def fake_kill(pid, signal):
        raise OSError("Access denied")

    monkeypatch.setattr(os, "kill", fake_kill)

    tool = CloseApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="close_application",
            parameters={"pid": 9999},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to close application"
    assert response.data["pid"] == 9999
    assert response.data["error"] == "Access denied"


def test_close_application_requires_tool_request():
    tool = CloseApplicationTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_close_application_requires_pid():
    tool = CloseApplicationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="close_application",
                parameters={},
            )
        )


def test_close_application_requires_integer_pid():
    tool = CloseApplicationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="close_application",
                parameters={"pid": "1234"},
            )
        )