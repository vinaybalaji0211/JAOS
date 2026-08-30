"""Canonical ExecutiveController execution-boundary coverage for F06D2C."""

from pathlib import Path
from unittest.mock import patch

import pytest

from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.executive.models import ExecutiveResponse
from jaos.tools.tool_manager import ToolManager


def test_deterministic_read_executes_through_canonical_tool_manager(
    tmp_path: Path,
) -> None:
    sample = tmp_path / "executive-controller-input.txt"
    sample.write_text("truthful canonical result", encoding="utf-8")

    tool_manager = ToolManager()
    load_tools(tool_manager)
    controller = ExecutiveController(tool_manager)

    with patch.object(
        tool_manager,
        "execute",
        wraps=tool_manager.execute,
    ) as execute:
        response = controller.process(f"read {sample}")

    execute.assert_called_once()
    assert isinstance(response, ExecutiveResponse)
    assert response.success is True
    assert response.message == "Task completed successfully."
    assert response.output == {
        "path": str(sample),
        "content": "truthful canonical result",
    }
    assert tuple(
        (record.tool_name, record.success)
        for record in tool_manager.list_audit_records()
    ) == (("read_file", True),)


def test_execution_metrics_record_truthful_real_tool_outcomes(
    tmp_path: Path,
) -> None:
    readable = tmp_path / "metrics-readable.txt"
    readable.write_text("metrics success", encoding="utf-8")
    missing = tmp_path / "metrics-missing.txt"

    tool_manager = ToolManager()
    load_tools(tool_manager)
    controller = ExecutiveController(tool_manager)

    with patch.object(
        tool_manager,
        "execute",
        wraps=tool_manager.execute,
    ) as execute:
        successful_response = controller.process(f"read {readable}")
        failed_response = controller.process(f"read {missing}")

    assert execute.call_count == 2
    assert successful_response.success is True
    assert successful_response.output == {
        "path": str(readable),
        "content": "metrics success",
    }
    assert failed_response.success is False
    assert failed_response.message == f"File does not exist: {missing}"
    assert failed_response.output is None

    metrics = controller.get_metrics()

    assert metrics.plans_executed == 2
    assert metrics.plans_succeeded == 1
    assert metrics.plans_failed == 1
    assert metrics.last_plan_steps == 1
    assert metrics.success_rate() == pytest.approx(0.5)
    assert tuple(
        (record.tool_name, record.success)
        for record in tool_manager.list_audit_records()
    ) == (("read_file", True), ("read_file", False))


@pytest.mark.parametrize("user_input", ("", " \t\r\n"))
def test_blank_input_fails_without_tool_manager_execution(
    user_input: str,
) -> None:
    tool_manager = ToolManager()
    load_tools(tool_manager)
    controller = ExecutiveController(tool_manager)

    with patch.object(
        tool_manager,
        "execute",
        wraps=tool_manager.execute,
    ) as execute:
        response = controller.process(user_input)

    execute.assert_not_called()
    assert isinstance(response, ExecutiveResponse)
    assert response.success is False
    assert response.message == "I don't know how to handle that request yet."
    assert response.output is None
    assert tool_manager.list_audit_records() == ()
