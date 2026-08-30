import subprocess

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.development.vscode.project_tool import (
    ProjectTool,
)


def test_project_tool_name():
    tool = ProjectTool()

    assert tool.tool_name == "project"


def test_project_success(tmp_path, monkeypatch):
    called = {}

    class DummyProcess:
        pid = 1234

    def fake_popen(command):
        called["command"] = command
        return DummyProcess()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    tool = ProjectTool()

    response = tool.execute(
        ToolRequest(
            tool_name="project",
            parameters={
                "project": str(tmp_path),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "VS Code project opened successfully"
    assert response.data["project"] == str(tmp_path)

    assert called["command"] == [
        "code",
        str(tmp_path),
    ]


def test_project_missing_directory(tmp_path):
    tool = ProjectTool()

    response = tool.execute(
        ToolRequest(
            tool_name="project",
            parameters={
                "project": str(tmp_path / "missing"),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Project path does not exist"


def test_project_launch_failure(tmp_path, monkeypatch):
    def fake_popen(command):
        raise OSError("VS Code not found")

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    tool = ProjectTool()

    response = tool.execute(
        ToolRequest(
            tool_name="project",
            parameters={
                "project": str(tmp_path),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to open VS Code project"
    assert response.data["error"] == "VS Code not found"


def test_project_requires_tool_request():
    tool = ProjectTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_project_requires_project():
    tool = ProjectTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="project",
                parameters={},
            )
        )


def test_project_rejects_empty_project():
    tool = ProjectTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="project",
                parameters={
                    "project": "   ",
                },
            )
        )