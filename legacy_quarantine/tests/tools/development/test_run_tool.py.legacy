import subprocess

import pytest

from executive_brain.tools.core.tool_models import ToolRequest, ToolStatus
from executive_brain.tools.development.vscode.run_tool import RunTool


def test_run_tool_name():
    assert RunTool().tool_name == "run"


def test_run_success(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python"],
        returncode=0,
        stdout="Program finished",
        stderr="",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = RunTool().execute(
        ToolRequest(
            tool_name="run",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Run completed successfully"
    assert response.data["stdout"] == "Program finished"


def test_run_failure(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python"],
        returncode=1,
        stdout="",
        stderr="Run failed",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = RunTool().execute(
        ToolRequest(
            tool_name="run",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Run failed"


def test_run_requires_tool_request():
    with pytest.raises(TypeError):
        RunTool().execute("invalid")


def test_run_requires_parameters():
    with pytest.raises(ValueError):
        RunTool().execute(
            ToolRequest(tool_name="run", parameters={})
        )