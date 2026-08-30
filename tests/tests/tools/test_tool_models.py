"""Canonical Tool Platform model requirements.

FORTRESS-06D2B migrated these requirements off the retired
``executive_brain.tools.core`` Tool Platform onto ``jaos.tools``. The legacy
payload is preserved byte-identically at
``legacy_quarantine/tests/tools/core/test_tool_models.py.legacy``.

Canonical mapping notes:

- Legacy ``ToolStatus`` carried execution outcome (``success``/``failure``).
  Canonical ``ToolStatus`` carries tool availability, and execution outcome
  moved to ``ToolResult.success``.
- Legacy ``ToolRequest.parameters`` is canonically ``ToolRequest.payload``.
- Legacy ``ToolResponse(status, message, data)`` is canonically
  ``ToolResult(success, output, error, created_at)``.
- The legacy blank-``tool_name`` rejection was enforced by the legacy
  ``ToolManager``. Canonical enforcement moved earlier, to ``ToolRequest``
  construction, so no request with a blank name can reach ``ToolManager``.
"""

from datetime import datetime, timezone

import pytest

from jaos.tools import (
    ToolRequest,
    ToolResult,
    ToolStatus,
)


def test_tool_status_values():
    """Canonical availability status values are stable strings."""

    assert ToolStatus.AVAILABLE.value == "available"
    assert ToolStatus.UNAVAILABLE.value == "unavailable"
    assert ToolStatus.DISABLED.value == "disabled"


def test_tool_request_defaults():
    """A request carries its tool name and defaults to an empty payload."""

    request = ToolRequest(tool_name="read_file")

    assert request.tool_name == "read_file"
    assert request.payload == {}
    assert request.approved is False


def test_tool_request_with_payload():
    """A request preserves the caller-supplied payload."""

    request = ToolRequest(
        tool_name="write_file",
        payload={
            "path": "notes.txt",
            "content": "Hello JAOS",
        },
    )

    assert request.tool_name == "write_file"
    assert request.payload["path"] == "notes.txt"
    assert request.payload["content"] == "Hello JAOS"


def test_tool_request_rejects_blank_tool_name():
    """Blank tool names are rejected at construction, before routing."""

    with pytest.raises(ValueError):
        ToolRequest(tool_name="   ")


def test_tool_result_defaults():
    """A result reports outcome and defaults to no output and no error."""

    result = ToolResult(success=True)

    assert result.success is True
    assert result.output is None
    assert result.error is None
    assert isinstance(result.created_at, datetime)
    assert result.created_at.tzinfo == timezone.utc


def test_tool_result_with_output():
    """A result preserves the tool-supplied output."""

    result = ToolResult(
        success=True,
        output={
            "size": 1024,
            "filename": "demo.txt",
        },
    )

    assert result.success is True
    assert result.output["size"] == 1024
    assert result.output["filename"] == "demo.txt"
    assert result.error is None
