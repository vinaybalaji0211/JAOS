import pytest

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)
from executive_brain.tools.core.tool_registry import ToolRegistry


class DummyTool(ToolInterface):
    def __init__(self, name: str = "dummy") -> None:
        self._name = name

    @property
    def tool_name(self) -> str:
        return self._name

    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Executed",
        )


def test_register_tool():
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    assert registry.has("dummy") is True
    assert registry.get("dummy") is tool


def test_register_invalid_tool():
    registry = ToolRegistry()

    with pytest.raises(TypeError):
        registry.register(object())


def test_register_duplicate_tool():
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.register(tool)


def test_unregister_tool():
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)
    registry.unregister("dummy")

    assert registry.has("dummy") is False


def test_unregister_missing_tool():
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.unregister("missing")


def test_get_missing_tool():
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_list_tools():
    registry = ToolRegistry()

    registry.register(DummyTool("read"))
    registry.register(DummyTool("write"))

    assert registry.list_tools() == ["read", "write"]


def test_count():
    registry = ToolRegistry()

    registry.register(DummyTool("one"))
    registry.register(DummyTool("two"))

    assert registry.count() == 2


def test_clear():
    registry = ToolRegistry()

    registry.register(DummyTool("one"))
    registry.register(DummyTool("two"))

    registry.clear()

    assert registry.count() == 0
    assert registry.list_tools() == []