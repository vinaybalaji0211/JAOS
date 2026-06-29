import subprocess

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.launch_application_tool import (
    LaunchApplicationTool,
)


class DummyProcess:
    def __init__(self, pid: int = 1234) -> None:
        self.pid = pid


def test_launch_application_tool_name():
    tool = LaunchApplicationTool()

    assert tool.tool_name == "launch_application"


def test_launch_application_success(monkeypatch):
    def fake_popen(application, cwd=None, shell=False):
        assert application == "notepad"
        assert cwd is None
        assert shell is True
        return DummyProcess(pid=999)

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    tool = LaunchApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="launch_application",
            parameters={"application": "notepad"},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Application launched successfully"
    assert response.data["application"] == "notepad"
    assert response.data["pid"] == 999


def test_launch_application_with_working_directory(tmp_path, monkeypatch):
    def fake_popen(application, cwd=None, shell=False):
        assert application == "cmd"
        assert cwd == str(tmp_path)
        assert shell is True
        return DummyProcess(pid=555)

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    tool = LaunchApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="launch_application",
            parameters={
                "application": "cmd",
                "working_directory": str(tmp_path),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.data["pid"] == 555


def test_launch_application_missing_working_directory(tmp_path):
    tool = LaunchApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="launch_application",
            parameters={
                "application": "cmd",
                "working_directory": str(tmp_path / "missing"),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Working directory does not exist"


def test_launch_application_requires_tool_request():
    tool = LaunchApplicationTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_launch_application_requires_application():
    tool = LaunchApplicationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="launch_application",
                parameters={},
            )
        )


def test_launch_application_rejects_empty_application():
    tool = LaunchApplicationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="launch_application",
                parameters={"application": "   "},
            )
        )


def test_launch_application_rejects_invalid_working_directory_value():
    tool = LaunchApplicationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="launch_application",
                parameters={
                    "application": "cmd",
                    "working_directory": "   ",
                },
            )
        )


def test_launch_application_failure(monkeypatch):
    def fake_popen(application, cwd=None, shell=False):
        raise OSError("launch failed")

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    tool = LaunchApplicationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="launch_application",
            parameters={"application": "bad-app"},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Application launch failed"
    assert response.data["error"] == "launch failed"