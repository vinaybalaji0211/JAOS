"""Canonical ToolManager requirements.

FORTRESS-06D2B migrated these requirements off the retired
``executive_brain.tools.core`` Tool Platform onto ``jaos.tools``. The legacy
payload is preserved byte-identically at
``legacy_quarantine/tests/tools/core/test_tool_manager.py.legacy``.

Canonical mapping notes:

- The legacy manager executed a tool directly. The canonical ``ToolManager``
  delegates to ``ToolExecutionEngine``, which enforces availability,
  permissions, and approval and then records an audit entry. These tests route
  every execution requirement through ``ToolManager`` so the authority chain is
  exercised rather than bypassed.
- Legacy unknown-tool routing raised ``KeyError``; canonical routing raises
  ``ToolNotFoundError``.
- Legacy ``list_tools`` returned a ``list``; canonical enumeration returns a
  sorted ``tuple``.
- The legacy blank-``tool_name`` guard now lives on ``ToolRequest``; see
  ``tests/tests/tools/test_tool_models.py``.

Permission, approval, and audit policy remains owned by FORTRESS-07 and is not
redefined here.
"""

import pytest

from jaos.tools import (
    ToolInterface,
    ToolManager,
    ToolMetadata,
    ToolNotFoundError,
    ToolRequest,
    ToolResult,
)


class ManagerProbeTool(ToolInterface):
    """Minimal canonical tool that echoes the routed request."""

    def __init__(self, name: str = "dummy") -> None:
        self._name = name

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name=self._name,
            version="1.0.0",
            description="Manager probe tool",
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(
            success=True,
            output={
                "executed_by": self._name,
                "requested": request.tool_name,
                "payload": request.payload,
            },
        )


def test_register_tool():
    """The manager owns registration and reports registered tools."""

    manager = ToolManager()

    manager.register_tool(ManagerProbeTool())

    assert manager.has_tool("dummy") is True


def test_list_tools():
    """The manager enumerates registered tools in canonical sorted form."""

    manager = ToolManager()

    manager.register_tool(ManagerProbeTool("write"))
    manager.register_tool(ManagerProbeTool("read"))

    assert manager.list_tools() == ("read", "write")


def test_execute_routes_request_to_the_registered_tool():
    """Execution reaches the named tool through the canonical chain."""

    manager = ToolManager()
    manager.register_tool(ManagerProbeTool("echo"))

    result = manager.execute(
        ToolRequest(
            tool_name="echo",
            payload={"text": "Hello"},
        )
    )

    assert result.success is True
    assert result.output == {
        "executed_by": "echo",
        "requested": "echo",
        "payload": {"text": "Hello"},
    }

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "echo"
    assert records[0].success is True
    assert records[0].error is None


def test_execute_unknown_tool():
    """Unknown tools fail at routing and never reach execution or audit."""

    manager = ToolManager()

    with pytest.raises(ToolNotFoundError):
        manager.execute(ToolRequest(tool_name="missing"))

    assert manager.list_audit_records() == ()
