import webbrowser

import pytest

from executive_brain.tools.browser.tabs_tool import TabsTool
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)


def test_tabs_tool_name():
    tool = TabsTool()

    assert tool.tool_name == "tabs"


def test_tabs_success(monkeypatch):
    opened = {}

    def fake_open_new_tab(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(webbrowser, "open_new_tab", fake_open_new_tab)

    tool = TabsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="tabs",
            parameters={
                "url": "https://openai.com",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Browser tab opened successfully"
    assert response.data["url"] == "https://openai.com"
    assert opened["url"] == "https://openai.com"


def test_tabs_browser_failure(monkeypatch):
    monkeypatch.setattr(webbrowser, "open_new_tab", lambda url: False)

    tool = TabsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="tabs",
            parameters={
                "url": "https://example.com",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to open browser tab"
    assert response.data["url"] == "https://example.com"


def test_tabs_requires_tool_request():
    tool = TabsTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_tabs_requires_url():
    tool = TabsTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="tabs",
                parameters={},
            )
        )


def test_tabs_rejects_empty_url():
    tool = TabsTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="tabs",
                parameters={
                    "url": "   ",
                },
            )
        )