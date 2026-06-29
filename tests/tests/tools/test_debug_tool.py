import subprocess

import pytest

from executive_brain.tools.core.tool_models import ToolRequest, ToolStatus
from executive_brain.tools.development.vscode.debug_tool import DebugTool


def test_debug_tool_name():
    assert DebugTool().tool_name == "debug"


def test_debug_success(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python"],
        returncode=0,
        stdout="Debug complete",
        stderr="",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = DebugTool().execute(
        ToolRequest(
            tool_name="debug",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Debug completed successfully"


def test_debug_failure(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["python"],
        returncode=1,
        stdout="",
        stderr="Debug failed",
    )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    response = DebugTool().execute(
        ToolRequest(
            tool_name="debug",
            parameters={
                "project": str(tmp_path),
                "command": ["python"],
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Debug failed"


def test_debug_requires_tool_request():
    with pytest.raises(TypeError):
        DebugTool().execute("invalid")


def test_debug_requires_parameters():
    with pytest.raises(ValueError):
        DebugTool().execute(
            ToolRequest(tool_name="debug", parameters={})
        )