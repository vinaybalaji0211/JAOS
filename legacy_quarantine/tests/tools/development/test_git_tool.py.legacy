import subprocess

import pytest

from executive_brain.tools.core.tool_models import ToolRequest, ToolStatus
from executive_brain.tools.development.vscode.git_tool import GitTool


def test_git_tool_name():
    assert GitTool().tool_name == "git"


def test_git_success(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["git", "status"],
        returncode=0,
        stdout="clean",
        stderr="",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = GitTool().execute(
        ToolRequest(
            tool_name="git",
            parameters={
                "repository": str(tmp_path),
                "command": ["status"],
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Git command completed successfully"


def test_git_failure(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["git"],
        returncode=1,
        stdout="",
        stderr="Git failed",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = GitTool().execute(
        ToolRequest(
            tool_name="git",
            parameters={
                "repository": str(tmp_path),
                "command": ["status"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Git command failed"


def test_git_requires_tool_request():
    with pytest.raises(TypeError):
        GitTool().execute("invalid")


def test_git_requires_parameters():
    with pytest.raises(ValueError):
        GitTool().execute(
            ToolRequest(tool_name="git", parameters={})
        )