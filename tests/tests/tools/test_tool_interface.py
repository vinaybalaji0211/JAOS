import pytest

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class DummyTool(ToolInterface):
    @property
    def tool_name(self) -> str:
        return "dummy"

    def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message=f"Executed {request.tool_name}",
        )


def test_tool_name():
    tool = DummyTool()

    assert tool.tool_name == "dummy"


def test_execute():
    tool = DummyTool()

    response = tool.execute(
        ToolRequest(tool_name="dummy")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Executed dummy"


def test_interface_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ToolInterface()