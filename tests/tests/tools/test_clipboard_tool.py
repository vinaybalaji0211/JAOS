import tkinter as tk

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.clipboard_tool import ClipboardTool


class FakeRoot:
    def __init__(self, text="Hello JAOS", raise_error=False):
        self._text = text
        self._raise_error = raise_error

    def withdraw(self):
        pass

    def clipboard_get(self):
        if self._raise_error:
            raise tk.TclError("Clipboard empty")
        return self._text

    def destroy(self):
        pass


def test_clipboard_tool_name():
    tool = ClipboardTool()

    assert tool.tool_name == "clipboard"


def test_clipboard_success(monkeypatch):
    monkeypatch.setattr(
        tk,
        "Tk",
        lambda: FakeRoot(text="Copied Text"),
    )

    tool = ClipboardTool()

    response = tool.execute(
        ToolRequest(tool_name="clipboard")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Clipboard read successfully"
    assert response.data["text"] == "Copied Text"
    assert response.data["length"] == len("Copied Text")


def test_clipboard_empty(monkeypatch):
    monkeypatch.setattr(
        tk,
        "Tk",
        lambda: FakeRoot(raise_error=True),
    )

    tool = ClipboardTool()

    response = tool.execute(
        ToolRequest(tool_name="clipboard")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.data["text"] == ""
    assert response.data["length"] == 0


def test_clipboard_requires_tool_request():
    tool = ClipboardTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")