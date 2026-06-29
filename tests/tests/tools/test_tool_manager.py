import pytest

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_manager import ToolManager
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class DummyTool(ToolInterface):
    def __init__(self, name: str = "dummy") -> None:
        self._name = name

    @property
    def tool_name(self) -> str:
        return self._name

    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message=f"{self.tool_name}: {request.tool_name}",
            data=request.parameters,
        )


def test_register_tool():
    manager = ToolManager()
    tool = DummyTool()

    manager.register_tool(tool)

    assert manager.has_tool("dummy") is True


def test_unregister_tool():
    manager = ToolManager()

    manager.register_tool(DummyTool())

    manager.unregister_tool("dummy")

    assert manager.has_tool("dummy") is False


def test_list_tools():
    manager = ToolManager()

    manager.register_tool(DummyTool("read"))
    manager.register_tool(DummyTool("write"))

    assert manager.list_tools() == ["read", "write"]


def test_execute_tool():
    manager = ToolManager()

    manager.register_tool(DummyTool("echo"))

    response = manager.execute(
        ToolRequest(
            tool_name="echo",
            parameters={"text": "Hello"},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "echo: echo"
    assert response.data == {"text": "Hello"}


def test_execute_unknown_tool():
    manager = ToolManager()

    with pytest.raises(KeyError):
        manager.execute(
            ToolRequest(tool_name="missing")
        )


def test_execute_invalid_request():
    manager = ToolManager()

    with pytest.raises(TypeError):
        manager.execute("invalid-request")


def test_execute_empty_tool_name():
    manager = ToolManager()

    with pytest.raises(ValueError):
        manager.execute(
            ToolRequest(tool_name="   ")
        )


def test_registry_property():
    manager = ToolManager()

    assert manager.registry is not None