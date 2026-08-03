import webbrowser

import pytest

from executive_brain.tools.browser.browser_automation_tool import (
    BrowserAutomationTool,
)
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)


def test_browser_automation_tool_name():
    tool = BrowserAutomationTool()

    assert tool.tool_name == "browser_automation"


def test_browser_open_success(monkeypatch):
    def fake_open(url):
        assert url == "https://openai.com"
        return True

    monkeypatch.setattr(webbrowser, "open", fake_open)

    tool = BrowserAutomationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="browser_automation",
            parameters={
                "url": "https://openai.com",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Browser opened successfully"
    assert response.data["url"] == "https://openai.com"


def test_browser_open_failure(monkeypatch):
    monkeypatch.setattr(webbrowser, "open", lambda url: False)

    tool = BrowserAutomationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="browser_automation",
            parameters={
                "url": "https://example.com",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to open browser"
    assert response.data["url"] == "https://example.com"


def test_browser_requires_tool_request():
    tool = BrowserAutomationTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_browser_requires_url():
    tool = BrowserAutomationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="browser_automation",
                parameters={},
            )
        )


def test_browser_rejects_empty_url():
    tool = BrowserAutomationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="browser_automation",
                parameters={
                    "url": "   ",
                },
            )
        )