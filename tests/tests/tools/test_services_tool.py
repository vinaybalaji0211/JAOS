import subprocess

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.services_tool import ServicesTool


def test_services_tool_name():
    tool = ServicesTool()

    assert tool.tool_name == "services"


def test_services_success(monkeypatch):
    sample_output = """
SERVICE_NAME: Appinfo
DISPLAY_NAME: Application Information
        TYPE               : 30  WIN32
        STATE              : 4  RUNNING

SERVICE_NAME: Spooler
DISPLAY_NAME: Print Spooler
        TYPE               : 110  WIN32_OWN_PROCESS
        STATE              : 1  STOPPED
"""

    completed = subprocess.CompletedProcess(
        args=["sc", "query", "type=", "service", "state=", "all"],
        returncode=0,
        stdout=sample_output,
        stderr="",
    )

    def fake_run(args, capture_output=False, text=False, check=False):
        assert args == ["sc", "query", "type=", "service", "state=", "all"]
        assert capture_output is True
        assert text is True
        assert check is False
        return completed

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ServicesTool()

    response = tool.execute(
        ToolRequest(tool_name="services")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Services listed successfully"
    assert response.data["count"] == 2
    assert response.data["services"][0]["service_name"] == "Appinfo"
    assert response.data["services"][0]["display_name"] == "Application Information"
    assert response.data["services"][0]["state"] == "4  RUNNING"
    assert response.data["services"][1]["service_name"] == "Spooler"
    assert response.data["services"][1]["state"] == "1  STOPPED"


def test_services_command_failure(monkeypatch):
    completed = subprocess.CompletedProcess(
        args=["sc", "query", "type=", "service", "state=", "all"],
        returncode=1,
        stdout="",
        stderr="failed",
    )

    def fake_run(args, capture_output=False, text=False, check=False):
        return completed

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ServicesTool()

    response = tool.execute(
        ToolRequest(tool_name="services")
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Service listing failed"
    assert response.data["returncode"] == 1
    assert response.data["stderr"] == "failed"


def test_services_os_error(monkeypatch):
    def fake_run(args, capture_output=False, text=False, check=False):
        raise OSError("sc unavailable")

    monkeypatch.setattr(subprocess, "run", fake_run)

    tool = ServicesTool()

    response = tool.execute(
        ToolRequest(tool_name="services")
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to list services"
    assert response.data["error"] == "sc unavailable"


def test_services_requires_tool_request():
    tool = ServicesTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_parse_services_output_empty():
    tool = ServicesTool()

    assert tool._parse_services_output("") == []


def test_parse_services_output_single_service():
    tool = ServicesTool()

    output = """
SERVICE_NAME: TestService
DISPLAY_NAME: Test Service
        STATE              : 4  RUNNING
"""

    services = tool._parse_services_output(output)

    assert len(services) == 1
    assert services[0]["service_name"] == "TestService"
    assert services[0]["display_name"] == "Test Service"
    assert services[0]["state"] == "4  RUNNING"