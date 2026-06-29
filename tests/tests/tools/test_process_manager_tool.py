import subprocess

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.process_manager_tool import (
    ProcessManagerTool,
)


def test_process_manager_tool_name():
    tool = ProcessManagerTool()

    assert tool.tool_name == "process_manager"


def test_process_manager_success(monkeypatch):
    sample_output = """
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
notepad.exe                   1234 Console                    1     10,000 K
python.exe                    5678 Console                    1     50,000 K
"""

    completed = subprocess.CompletedProcess(
        args=["tasklist"],
        returncode=0,
        stdout=sample_output,
        stderr="",
    )

    def fake_run(args, capture_output=False, text=False, check=False):
        assert args == ["tasklist"]
        assert capture_output is True
        assert text is True
        assert check is False
        return completed

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ProcessManagerTool()

    response = tool.execute(
        ToolRequest(tool_name="process_manager")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Processes listed successfully"
    assert response.data["count"] == 3
    assert response.data["processes"][1]["image_name"] == "notepad.exe"
    assert response.data["processes"][1]["pid"] == "1234"


def test_process_manager_command_failure(monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["tasklist"],
        returncode=1,
        stdout="",
        stderr="failed",
    )

    def fake_run(args, capture_output=False, text=False, check=False):
        return completed

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ProcessManagerTool()

    response = tool.execute(
        ToolRequest(tool_name="process_manager")
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Process listing failed"
    assert response.data["returncode"] == 1
    assert response.data["stderr"] == "failed"


def test_process_manager_os_error(monkeypatch):
    def fake_run(args, capture_output=False, text=False, check=False):
        raise OSError("tasklist unavailable")

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ProcessManagerTool()

    response = tool.execute(
        ToolRequest(tool_name="process_manager")
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to list processes"
    assert response.data["error"] == "tasklist unavailable"


def test_process_manager_requires_tool_request():
    tool = ProcessManagerTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_parse_tasklist_output_skips_invalid_lines():
    tool = ProcessManagerTool()

    output = """
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
invalid
explorer.exe                  1000 Console                    1     20,000 K
"""

    processes = tool._parse_tasklist_output(output)

    assert len(processes) == 1
    assert processes[0]["image_name"] == "explorer.exe"
    assert processes[0]["pid"] == "1000"