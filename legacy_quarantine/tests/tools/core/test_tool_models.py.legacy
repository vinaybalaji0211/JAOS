from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


def test_tool_status_values():
    assert ToolStatus.SUCCESS.value == "success"
    assert ToolStatus.FAILURE.value == "failure"


def test_tool_request_defaults():
    request = ToolRequest(tool_name="read_file")

    assert request.tool_name == "read_file"
    assert request.parameters == {}


def test_tool_request_with_parameters():
    request = ToolRequest(
        tool_name="write_file",
        parameters={
            "path": "notes.txt",
            "content": "Hello JAOS",
        },
    )

    assert request.tool_name == "write_file"
    assert request.parameters["path"] == "notes.txt"
    assert request.parameters["content"] == "Hello JAOS"


def test_tool_response_defaults():
    response = ToolResponse(
        status=ToolStatus.SUCCESS,
        message="Completed",
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Completed"
    assert response.data == {}


def test_tool_response_with_data():
    response = ToolResponse(
        status=ToolStatus.SUCCESS,
        message="Done",
        data={
            "size": 1024,
            "filename": "demo.txt",
        },
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Done"
    assert response.data["size"] == 1024
    assert response.data["filename"] == "demo.txt"
