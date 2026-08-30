"""Canonical ToolInterface contract requirements.

FORTRESS-06D2B migrated these requirements off the retired
``executive_brain.tools.core`` Tool Platform onto ``jaos.tools``. The legacy
payload is preserved byte-identically at
``legacy_quarantine/tests/tools/core/test_tool_interface.py.legacy``.

Canonical mapping notes:

- Legacy tool identity came from a ``tool_name`` property. Canonical identity
  is declared through ``ToolInterface.metadata()``.
- Legacy execution returned ``ToolResponse(status, message, data)``. Canonical
  execution returns ``ToolResult(success, output, error)``.
"""

import pytest

from jaos.tools import (
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class EchoInterfaceTool(ToolInterface):
    """Minimal canonical tool used to exercise the interface contract."""

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="echo_interface",
            version="1.0.0",
            description="Interface contract probe tool",
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(
            success=True,
            output=request.payload,
        )


class MetadataOnlyTool(ToolInterface):
    """Implements only ``metadata`` and must remain abstract."""

    def metadata(self) -> ToolMetadata:  # pragma: no cover - never constructed
        return ToolMetadata(
            name="metadata_only",
            version="1.0.0",
            description="Incomplete tool",
        )


def test_tool_interface_cannot_be_instantiated():
    """The canonical tool contract stays abstract."""

    with pytest.raises(TypeError):
        ToolInterface()


def test_partial_tool_implementation_cannot_be_instantiated():
    """Both ``metadata`` and ``execute`` are required to build a tool."""

    with pytest.raises(TypeError):
        MetadataOnlyTool()


def test_tool_identity_is_declared_through_metadata():
    """Canonical tool identity replaces the legacy ``tool_name`` property."""

    metadata = EchoInterfaceTool().metadata()

    assert isinstance(metadata, ToolMetadata)
    assert metadata.name == "echo_interface"
    assert metadata.version == "1.0.0"
    assert metadata.description == "Interface contract probe tool"


def test_tool_execute_returns_canonical_result_for_the_request():
    """``execute`` accepts a ``ToolRequest`` and returns a ``ToolResult``."""

    result = EchoInterfaceTool().execute(
        ToolRequest(
            tool_name="echo_interface",
            payload={"text": "Hello JAOS"},
        )
    )

    assert isinstance(result, ToolResult)
    assert result.success is True
    assert result.output == {"text": "Hello JAOS"}
    assert result.error is None
