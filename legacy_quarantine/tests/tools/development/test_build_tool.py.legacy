import subprocess

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.development.vscode.build_tool import (
    BuildTool,
)


def test_build_tool_name():
    tool = BuildTool()

    assert tool.tool_name == "build"


def test_build_success(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python", "-m", "build"],
        returncode=0,
        stdout="Build successful",
        stderr="",
    )

    def fake_run(command, cwd=None, capture_output=False, text=False, check=False):
        assert command == ["python", "-m", "build"]
        assert cwd == str(tmp_path)
        assert capture_output is True
        assert text is True
        assert check is False
        return completed

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = BuildTool()

    response = tool.execute(
        ToolRequest(
            tool_name="build",
            parameters={
                "project": str(tmp_path),
                "command": ["python", "-m", "build"],
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Build completed successfully"
    assert response.data["stdout"] == "Build successful"


def test_build_failure(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python"],
        returncode=1,
        stdout="",
        stderr="Build failed",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    tool = BuildTool()

    response = tool.execute(
        ToolRequest(
            tool_name="build",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Build failed"
    assert response.data["returncode"] == 1
    assert response.data["stderr"] == "Build failed"


def test_build_os_error(tmp_path, monkeypatch):
    def fake_run(*args, **kwargs):
        raise OSError("command not found")

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = BuildTool()

    response = tool.execute(
        ToolRequest(
            tool_name="build",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Build execution failed"
    assert response.data["error"] == "command not found"


def test_build_missing_project(tmp_path):
    tool = BuildTool()

    response = tool.execute(
        ToolRequest(
            tool_name="build",
            parameters={
                "project": str(tmp_path / "missing"),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Project path does not exist"


def test_build_requires_tool_request():
    tool = BuildTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_build_requires_project():
    tool = BuildTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="build",
                parameters={
                    "command": ["python"],
                },
            )
        )


def test_build_requires_command():
    tool = BuildTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="build",
                parameters={
                    "project": ".",
                    "command": [],
                },
            )
        )