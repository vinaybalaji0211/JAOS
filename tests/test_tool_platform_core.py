import pytest

from jaos.tools import (
    ToolAlreadyRegisteredError,
    ToolDisabledError,
    ToolInterface,
    ToolManager,
    ToolMetadata,
    ToolNotFoundError,
    ToolRegistry,
    ToolRequest,
    ToolResult,
    ToolStatus,
)


class EchoTool(ToolInterface):
    def __init__(self, status: ToolStatus = ToolStatus.AVAILABLE) -> None:
        self._status = status

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="echo",
            version="1.0.0",
            description="Echo test tool",
            status=self._status,
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(
            success=True,
            output=request.payload,
        )


def test_tool_metadata_rejects_empty_name():
    with pytest.raises(ValueError):
        ToolMetadata(name=" ", version="1.0.0", description="desc")


def test_tool_metadata_rejects_empty_version():
    with pytest.raises(ValueError):
        ToolMetadata(name="tool", version=" ", description="desc")


def test_tool_metadata_rejects_empty_description():
    with pytest.raises(ValueError):
        ToolMetadata(name="tool", version="1.0.0", description=" ")


def test_tool_request_rejects_empty_name():
    with pytest.raises(ValueError):
        ToolRequest(tool_name=" ")


def test_tool_registry_register_and_get():
    registry = ToolRegistry()
    tool = EchoTool()

    registry.register(tool)

    assert registry.has("echo") is True
    assert registry.get("echo") is tool
    assert registry.list_tools() == ("echo",)


def test_tool_registry_normalizes_names():
    registry = ToolRegistry()
    tool = EchoTool()

    registry.register(tool)

    assert registry.has(" ECHO ") is True


def test_tool_registry_rejects_duplicate():
    registry = ToolRegistry()
    tool = EchoTool()

    registry.register(tool)

    with pytest.raises(ToolAlreadyRegisteredError):
        registry.register(tool)


def test_tool_registry_missing_tool():
    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.get("missing")


def test_tool_manager_executes_tool():
    manager = ToolManager()
    manager.register_tool(EchoTool())

    result = manager.execute(
        ToolRequest(
            tool_name="echo",
            payload={"message": "hello"},
        )
    )

    assert result.success is True
    assert result.output == {"message": "hello"}


def test_tool_manager_rejects_disabled_tool():
    manager = ToolManager()
    manager.register_tool(EchoTool(status=ToolStatus.DISABLED))

    with pytest.raises(ToolDisabledError):
        manager.execute(ToolRequest(tool_name="echo"))